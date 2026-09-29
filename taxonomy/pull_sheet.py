"""
Pull the taxonomy annotation sheet from Google Sheets into taxonomy/annotation_sheet.csv.

The sheet is the working surface for annotation; the committed CSV is the frozen record that the
analysis reads.

Usage:
    uv run python taxonomy/pull_sheet.py                # first tab, default output path
    uv run python taxonomy/pull_sheet.py --gid 123456   # a specific tab (gid is in the tab URL)
    uv run python taxonomy/pull_sheet.py --check        # report differences, write nothing
"""

import argparse
import csv
import io
import sys
import urllib.error
import urllib.request
from pathlib import Path

SHEET_ID = "1wPJQEQHTMulkVwAT1RbsJdcIyLWiV8egwoYeIhpZAL8"
DEFAULT_OUT = Path(__file__).resolve().parent / "annotation_sheet.csv"
TIMEOUT_S = 30


def export_url(sheet_id: str, gid: str | None) -> str:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return f"{url}&gid={gid}" if gid is not None else url


def fetch_csv(url: str) -> str:
    """
    Download the sheet as CSV text, failing loudly if Google returns anything else.
    """
    req = urllib.request.Request(url, headers={"User-Agent": "pariah/pull_sheet"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            content_type = resp.headers.get("Content-Type", "")
            body = resp.read().decode("utf-8-sig")
    except urllib.error.HTTPError as e:
        raise SystemExit(
            f"HTTP {e.code} fetching the sheet. Check that link sharing is set to "
            f"'Anyone with the link: Viewer' and that the sheet id / gid are correct."
        ) from e
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error fetching the sheet: {e.reason}") from e
    # A private sheet redirects to an HTML login page with status 200.
    if "csv" not in content_type.lower() or body.lstrip().lower().startswith("<!doctype html"):
        raise SystemExit(
            f"Expected CSV but got Content-Type {content_type!r}. "
            "The sheet is probably not shared publicly."
        )
    return body


def normalize(text: str) -> tuple[list[str], list[list[str]]]:
    """
    Parse CSV text and drop fully empty rows and trailing empty columns.
    """
    rows = [r for r in csv.reader(io.StringIO(text)) if any(c.strip() for c in r)]
    if not rows:
        raise SystemExit("The sheet is empty.")
    header = rows[0]
    width = len(header)
    while width > 0 and not header[width - 1].strip():
        width -= 1
    if width == 0:
        raise SystemExit("The first row (header) is empty.")
    header = [h.strip() for h in header[:width]]
    if len(set(header)) != len(header):
        dups = sorted({h for h in header if header.count(h) > 1})
        raise SystemExit(f"Duplicate column names in the header: {dups}")
    body = [(r + [""] * width)[:width] for r in rows[1:]]
    return header, [[c.strip() for c in r] for r in body]


def render(header: list[str], body: list[list[str]]) -> str:
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(body)
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--sheet-id", default=SHEET_ID)
    ap.add_argument("--gid", default=None, help="tab id; default is the first tab")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true", help="report changes, do not write")
    args = ap.parse_args()

    header, body = normalize(fetch_csv(export_url(args.sheet_id, args.gid)))
    new_text = render(header, body)
    old_text = args.out.read_text(encoding="utf-8") if args.out.exists() else ""

    if new_text == old_text:
        print(f"No changes ({len(body)} rows, {len(header)} columns).")
        return 0
    print(f"Sheet: {len(body)} rows, {len(header)} columns. Columns: {', '.join(header)}")
    if args.check:
        print(f"{args.out} differs from the sheet (--check, nothing written).")
        return 1
    # Write atomically so an interrupted run never leaves a half-written record.
    tmp = args.out.with_suffix(".csv.tmp")
    tmp.write_text(new_text, encoding="utf-8", newline="")
    tmp.replace(args.out)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
