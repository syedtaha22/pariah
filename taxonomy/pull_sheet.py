"""
Pull the taxonomy tabs from Google Sheets into CSV files in taxonomy/.

The sheet is the working surface for annotation and screening; the committed CSVs are the frozen
record that the analysis reads.

Usage:
    uv run python taxonomy/pull_sheet.py                    # pull every tab
    uv run python taxonomy/pull_sheet.py --tab screening    # pull one tab (repeatable)
    uv run python taxonomy/pull_sheet.py --check            # report differences, write nothing
"""

import argparse
import csv
import io
import sys
import urllib.error
import urllib.request
from pathlib import Path

SHEET_ID = "1oLs2gFi7dHppirYe85IIiVnHk7T8rR8FWzJ5L6e9kAc"
OUT_DIR = Path(__file__).resolve().parent / "data"
TIMEOUT_S = 30

# Tab name -> (gid, is_table, expected first header cell). Tables have one header row and one
# record per row. A report tab is written as it appears, apart from trailing empty columns.
TABS = {
    "annotation": ("385185777", True, "paper_id"),
    "search_log": ("1473108103", True, "date"),
    "screening": ("1676657732", True, "candidate_id"),
    "counts": ("1906502540", False, "Stage"),
}


def export_url(sheet_id: str, gid: str) -> str:
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"


def fetch_csv(url: str) -> str:
    """
    Download a tab as CSV text, failing loudly if Google returns anything else.
    """
    req = urllib.request.Request(url, headers={"User-Agent": "pariah/pull_sheet"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            content_type = resp.headers.get("Content-Type", "")
            body = resp.read().decode("utf-8-sig")
    except urllib.error.HTTPError as e:
        raise SystemExit(
            f"HTTP {e.code} fetching the sheet. Check that link sharing is set to "
            f"'Anyone with the link: Viewer' and that the sheet id and tab id are correct."
        ) from e
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error fetching the sheet: {e.reason}") from e
    # A private sheet answers with an HTML login page and status 200.
    if "csv" not in content_type.lower() or body.lstrip().lower().startswith("<!doctype html"):
        raise SystemExit(
            f"Expected CSV but got Content-Type {content_type!r}. "
            "The sheet is probably not shared publicly."
        )
    return body


def trim(rows: list[list[str]]) -> list[list[str]]:
    """
    Strip cell whitespace and remove trailing empty columns shared by all rows.
    """
    rows = [[c.strip() for c in r] for r in rows]
    width = max((len(r) for r in rows), default=0)
    rows = [r + [""] * (width - len(r)) for r in rows]
    while width > 0 and all(not r[width - 1] for r in rows):
        width -= 1
    return [r[:width] for r in rows]


def normalize_table(tab: str, text: str, first_header: str) -> list[list[str]]:
    """
    Parse a table tab: drop fully empty rows and validate the header.
    """
    rows = [r for r in csv.reader(io.StringIO(text)) if any(c.strip() for c in r)]
    rows = trim(rows)
    if not rows:
        raise SystemExit(f"Tab '{tab}' is empty.")
    header = rows[0]
    if header[0] != first_header:
        raise SystemExit(
            f"Tab '{tab}' starts with column '{header[0]}' but '{first_header}' was expected. "
            "The tab name may be wrong, or its header row was changed."
        )
    if "" in header:
        raise SystemExit(f"Tab '{tab}' has an empty column name in its header.")
    if len(set(header)) != len(header):
        dups = sorted({h for h in header if header.count(h) > 1})
        raise SystemExit(f"Tab '{tab}' has duplicate column names: {dups}")
    return rows


def normalize_report(tab: str, text: str, first_header: str) -> list[list[str]]:
    """
    Parse a report tab, keeping its layout and validating the first cell.
    """
    rows = trim(list(csv.reader(io.StringIO(text))))
    if not rows or rows[0][0] != first_header:
        raise SystemExit(f"Tab '{tab}' does not start with '{first_header}'.")
    return rows


def render(rows: list[list[str]]) -> str:
    buf = io.StringIO(newline="")
    csv.writer(buf, lineterminator="\n").writerows(rows)
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--sheet-id", default=SHEET_ID)
    ap.add_argument(
        "--tab", action="append", choices=list(TABS), help="tab to pull; default is every tab"
    )
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR)
    ap.add_argument("--check", action="store_true", help="report changes, do not write")
    args = ap.parse_args()

    # Fetch and validate every tab before writing anything, so a failure leaves all files as
    # they were.
    pending: dict[Path, str] = {}
    for tab in args.tab or list(TABS):
        gid, is_table, first_header = TABS[tab]
        text = fetch_csv(export_url(args.sheet_id, gid))
        parse = normalize_table if is_table else normalize_report
        rows = parse(tab, text, first_header)
        pending[args.out_dir / f"{tab}.csv"] = render(rows)
        records = len(rows) - 1 if is_table else len(rows)
        print(f"{tab}: {records} {'records' if is_table else 'rows'}, {len(rows[0])} columns")

    changed = []
    for path, new_text in pending.items():
        old_text = path.read_text(encoding="utf-8") if path.exists() else None
        if new_text != old_text:
            changed.append(path)

    if not changed:
        print("No changes.")
        return 0
    if args.check:
        for path in changed:
            print(f"differs from the sheet: {path.name}")
        return 1
    # Write atomically so an interrupted run never leaves a half-written file.
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for path in changed:
        tmp = path.with_suffix(".csv.tmp")
        tmp.write_text(pending[path], encoding="utf-8", newline="")
        tmp.replace(path)
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
