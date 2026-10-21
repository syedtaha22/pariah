import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "pull_sheet", Path(__file__).resolve().parents[1] / "taxonomy" / "pull_sheet.py"
)
pull_sheet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pull_sheet)

HEADER = ["candidate_id", "citation", "found_via", "duplicate_of"]


def table(*rows):
    return [HEADER, *[list(r) for r in rows]]


def test_consistent_table_passes():
    rows = table(
        ("NK-001", "A. One. X 2020", "1", ""),
        ("ST-001", "B. Two. Y 2021", "2", ""),
        ("ST-002", "A. One. X 2020", "3", "NK-001"),
        ("ST-003", "B. Two. Y 2021", "3", "ST-001"),
    )
    assert pull_sheet.check_screening(rows) == []


def test_ids_must_increase_within_a_prefix():
    rows = table(("ST-002", "A", "1", ""), ("ST-001", "B", "1", ""), ("NK-001", "C", "1", ""))
    problems = pull_sheet.check_screening(rows)
    assert len(problems) == 1 and "ST-001 comes after ST-002" in problems[0]


def test_repeated_and_malformed_ids():
    rows = table(("ST-001", "A", "1", ""), ("ST-001", "B", "1", ""), ("001", "C", "1", ""))
    problems = pull_sheet.check_screening(rows)
    assert any("already appears" in p for p in problems)
    assert any("does not look like" in p for p in problems)


def test_duplicate_must_point_to_an_earlier_row():
    rows = table(("ST-001", "A", "1", "ST-002"), ("ST-002", "A", "1", ""))
    assert any("should come before" in p for p in pull_sheet.check_screening(rows))
    rows = table(("ST-001", "A", "1", "ST-009"))
    assert any("not in the sheet" in p for p in pull_sheet.check_screening(rows))
    rows = table(("ST-001", "A", "1", "ST-001"))
    assert any("should come before" in p for p in pull_sheet.check_screening(rows))


def test_duplicate_citation_must_match_exactly():
    rows = table(("ST-001", "A. One. X 2020", "1", ""), ("ST-002", "A. One. X 2021", "2", "ST-001"))
    problems = pull_sheet.check_screening(rows)
    assert len(problems) == 1 and "citations differ" in problems[0]


def test_duplicate_must_not_point_to_a_duplicate():
    rows = table(
        ("ST-001", "A", "1", ""),
        ("ST-002", "A", "1", "ST-001"),
        ("ST-003", "A", "1", "ST-002"),
    )
    problems = pull_sheet.check_screening(rows)
    assert len(problems) == 1 and "itself a duplicate" in problems[0]
