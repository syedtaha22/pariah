# Pariah

**SoK: On the Generalization and Limits of GNN-Transformer Hybrids in Intrusion Detection**

Authors: Syed Taha, Fatima Kaleem, Nawail Khan.

This project tests whether hybrids of graph neural networks (GNNs) and Transformers stay reliable
for network intrusion detection when the deployment network differs from the training network,
and whether invariance-based training (IRM, EERM, DIR) improves them beyond tuned empirical risk
minimization (ERM) and Group DRO.

## Contributions

1. **Taxonomy.** A systematization of GNN, Transformer and hybrid intrusion detectors, organized
   by graph construction, local and global mechanism, and evaluation protocol. See
   [taxonomy/](taxonomy/).
2. **Benchmark.** A reproducible benchmark made of:
   - cleaned NetFlow intrusion data,
   - documented environment splits,
   - a synthetic shift generator with known causal and spurious structure.
3. **Controlled evaluation.** A comparison of invariance objectives (IRM, EERM, DIR) against
   tuned empirical risk minimization (ERM) and Group DRO, applied to GNN-Transformer hybrids under
   topology and size shift.

## Hypotheses

Each hypothesis is paired with a null hypothesis. Effects are assessed over at least 10 random
seeds per configuration, with paired bootstrap confidence intervals and Holm correction across
hypotheses. All methods receive the same hyperparameter budget. The evaluation protocol is in
[protocol.md](protocol.md).

### H1: invariance objectives (primary)

- **Alternative (H1):** integrating invariant representation learning objectives into
  GNN-Transformer hybrids lowers the false-positive rate at a fixed true-positive rate and raises
  worst-environment F1 on held-out networks, compared with the same hybrids trained by tuned ERM
  or Group DRO, without reducing in-distribution performance beyond a pre-stated tolerance.
- **Null (H0):** invariance objectives do not differ from tuned ERM or Group DRO on these metrics.

### H1.1: structural scaling

- **Alternative (H1.1):** with architecture, attention type and training held fixed, size-robust
  positional and structural encodings yield higher worst-size-bin F1 than standard encodings when
  testing on networks 2x, 5x and 10x larger than the training networks.
- **Null (H0.1):** the choice of positional or structural encoding has no statistically
  significant effect on worst-size-bin F1 under these size shifts.

### H1.2: spurious shortcut mitigation

- **Alternative (H1.2):** enforcing IRM or conditional invariance penalties across diverse
  environmental graph partitions reduces a hybrid's reliance on injected non-causal global
  structure, measured as the accuracy drop when that structure is removed or randomized, relative
  to a matched non-invariant regularizer and to standard cross-entropy training.
- **Null (H0.2):** invariant risk penalties do not change this interventional reliance measure
  relative to a matched non-invariant regularizer or standard cross-entropy training.

## Layout

```
.
├── configs/
├── data
│   ├── processed/
│   └── raw/
├── experiments/
├── paper
│   └── proposal/
├── src
│   ├── data/
│   ├── eval/
│   ├── models/
│   ├── objectives/
│   └── utils
│       ├── config.py
│       ├── logger.py
│       └── seed.py
├── taxonomy
│   ├── annotation.csv
│   ├── counts.csv
│   ├── pull_sheet.py
│   ├── README.md
│   ├── screening.csv
│   ├── search_log.csv
│   └── selection_criteria.md
├── tests
│   └── test_utils.py
├── .gitignore
├── protocol.md
├── pyproject.toml
├── .python-version
├── README.md
└── uv.lock
```

## Setup

Requires [uv](https://docs.astral.sh/uv/). Python 3.12 is pinned in `.python-version`.

```bash
uv sync            # creates .venv from pyproject.toml and uv.lock (CUDA 12.8 torch wheels)
uv run pytest      # unit tests
uv run ruff check  # lint
```

`uv.lock` is committed and is the record of the exact environment. Change dependencies with
`uv add <pkg>` so the lockfile stays in sync.

## Reproducibility conventions

- Every run is driven by a YAML config in `configs/`; the config hash and seed are logged with
  every result row (`src/utils/config.py`, `src/utils/logger.py`).
- All randomness goes through `seed_everything` (`src/utils/seed.py`).
- Results are appended to CSV files, one row per evaluation.
