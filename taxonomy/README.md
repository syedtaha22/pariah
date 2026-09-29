# Taxonomy

This folder holds the systematization part of the project (Deliverable 1 of the proposal): a
structured classification of GNN, Transformer and hybrid intrusion detectors, organized by graph
construction, local and global mechanism, and evaluation protocol. It also provides the evidence
for the research gap, for example how many surveyed papers evaluate only in-distribution.

Status: the sheet contains the column header only. No papers have been annotated yet.

## How it works

Two copies of the data exist, and each has one job.

| Copy | Job |
| --- | --- |
| [Google Sheet](https://docs.google.com/spreadsheets/d/1wPJQEQHTMulkVwAT1RbsJdcIyLWiV8egwoYeIhpZAL8/edit?usp=sharing) | Working surface. All annotation and editing happens here. |
| `annotation_sheet.csv` | Frozen record. Committed to git and read by the analysis code. |

The CSV should not be edited by hand. It should be produced from the sheet by `pull_sheet.py`, so the two
cannot silently diverge and every change to the record is a reviewable git diff.

## Files

- `annotation_sheet.csv`: one row per surveyed paper, one column per attribute.
- `pull_sheet.py`: downloads the sheet as CSV into `annotation_sheet.csv`.
- `README.md`: this file.

## Usage

Run from the repository root. The sheet must be shared as "Anyone with the link: Viewer".

```bash
uv run python taxonomy/pull_sheet.py             # pull the first tab into annotation_sheet.csv
uv run python taxonomy/pull_sheet.py --check     # report differences, write nothing (exit 1 if any)
uv run python taxonomy/pull_sheet.py --gid 123   # pull a specific tab (gid is in the tab URL)
uv run python taxonomy/pull_sheet.py --out path  # write somewhere else
```

Workflow:
1. Annotate papers in the sheet.
2. Run `--check` to see whether the committed CSV is behind.
3. Run the script without flags, review the diff with `git diff taxonomy/annotation_sheet.csv`, and
   commit it.

## Columns

The columns follow the taxonomy axes. These are the initial columns, and the allowed values for
each will be fixed before annotation starts.

| Group | Column | Meaning |
| --- | --- | --- |
| Identity | `paper_id` | Stable id for the paper in this study |
| | `citation_key` | Key in `paper/proposal/references.bib` |
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
