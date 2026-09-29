"""
Append-only CSV run logger.

Every row is one record (for example one evaluation of one run). The header is fixed by the
first row written; later rows must use the same keys, so result files stay machine-readable.
"""

import csv
from pathlib import Path
from typing import Any


class CSVLogger:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fields: list[str] | None = None
        if self.path.exists() and self.path.stat().st_size > 0:
            with open(self.path, newline="", encoding="utf-8") as f:
                self._fields = next(csv.reader(f))

    def log(self, row: dict[str, Any]) -> None:
        if self._fields is None:
            self._fields = list(row)
            with open(self.path, "w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=self._fields).writeheader()
        elif set(row) != set(self._fields):
            raise ValueError(
                f"Row keys {sorted(row)} do not match log header {sorted(self._fields)}"
            )
        with open(self.path, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=self._fields).writerow(row)
