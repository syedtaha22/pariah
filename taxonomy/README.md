# Taxonomy

This folder holds the systematization part of the project (Deliverable 1 of the proposal): a
structured classification of GNN, Transformer and hybrid intrusion detectors, organized by graph
construction, local and global mechanism, and evaluation protocol. It also provides the evidence
for the research gap, for example how many surveyed papers evaluate only in-distribution.

Status: no papers have been annotated yet.

## How it works

Two copies of the data exist, and each has one job.

| Copy | Job |
| --- | --- |
| [Google Sheet](https://docs.google.com/spreadsheets/d/1oLs2gFi7dHppirYe85IIiVnHk7T8rR8FWzJ5L6e9kAc/edit?usp=sharing) | Working surface. All annotation and screening happens here. |
| The CSV files in [data/](data/) | Frozen record. Committed to git and read by the analysis code. |

The CSV files should not be edited by hand. They should be produced from the sheet by
[pull_sheet.py](pull_sheet.py), so the two cannot silently diverge and every change to the record
is a reviewable git diff.

The sheet has five tabs:

| Tab | Contents | CSV |
| --- | --- | --- |
| `annotation` | One row per included paper, one column per attribute | `data/annotation.csv` |
| `search_log` | One row per search or citation chase | `data/search_log.csv` |
| `screening` | One row per candidate paper, with its screening decisions | `data/screening.csv` |
| `counts` | Screening totals and exclusions by reason, computed by formulas | `data/counts.csv` |
| `guide` | Explains every column and reason code | none |

## Files

- [selection_criteria.md](selection_criteria.md): scope, date range, sources, search terms, and the
  inclusion and exclusion criteria.
- [pull_sheet.py](pull_sheet.py): downloads the tabs of the sheet into the CSV files in `data/`.
- [data/](data/): `annotation.csv`, `search_log.csv`, `screening.csv` and `counts.csv`, the record.
- `README.md`: this file.

## Usage

Run from the repository root. The sheet must be shared as "Anyone with the link: Viewer".

```bash
uv run python taxonomy/pull_sheet.py                   # pull every tab
uv run python taxonomy/pull_sheet.py --tab screening   # pull one tab (repeatable)
uv run python taxonomy/pull_sheet.py --check           # report differences, write nothing (exit 1 if any)
uv run python taxonomy/pull_sheet.py --out-dir path    # write somewhere else
```

Every tab is fetched and checked before anything is written, so a failure leaves all files as they
were.

Workflow:
1. Annotate papers and record screening in the sheet.
2. Run `--check` to see whether the committed CSV files are behind.
3. Run the script without flags, review the diff with `git diff taxonomy/data/`, and commit it.

## Columns

The columns follow the taxonomy axes. These are the initial columns, and the allowed values for
each will be fixed before annotation starts.

| Group | Column | Meaning |
| --- | --- | --- |
| Identity | `paper_id` | Stable id for the paper in this study |
| | `citation_key` | Key in [references.bib](../paper/references.bib) |
| | `year`, `venue` | Publication year and venue |
| | `domain` | Network traffic or provenance |
| Graph construction | `graph_construction` | What the nodes and edges represent |
| | `node_features`, `edge_features` | What features are used |
| Local mechanism | `local_mechanism` | Message passing type (GCN, SAGE, GAT, GIN, ...) |
| Global mechanism | `global_mechanism` | Global attention type (none, full, sparse, ...) |
| | `positional_encoding` | Positional or structural encoding used |
| Evaluation protocol | `datasets` | Datasets used |
| | `split_protocol` | How train and test are separated (random, temporal, cross-dataset, ...) |
| | `ood_evaluation` | Whether and how shift is evaluated |
| | `metrics` | Reported metrics |
| | `tuning_fairness` | Whether baselines get an equal tuning budget |
| | `seeds` | Number of seeds reported |
| | `code_available` | Whether code is released |
| Bookkeeping | `include` | Whether the paper is in the final set |
| | `notes` | Free text |
