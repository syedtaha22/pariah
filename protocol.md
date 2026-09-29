# Evaluation protocol (to be frozen before any experiment)

Status: DRAFT stub. 

## Fields to freeze

- Fixed TPR at which FPR is compared: TBD
- In-distribution tolerance (maximum acceptable drop): TBD
- Primary metrics: worst-environment F1, FPR at fixed TPR, worst-size-bin F1
- Secondary metrics: AUROC, AUPRC, interventional reliance drop, attention mass on injected structure
- Model selection: source-environment validation (primary); OOD validation reported separately
- Seeds: at least 10 per configuration; seed list: TBD
- Statistics: paired bootstrap CIs (resamples: TBD), Holm correction over the hypothesis family (family definition: TBD)
- Hyperparameter budget: number of trials, search space rules and search method, identical for all methods: TBD
- Environment definitions for real data (dataset, subnet, time window, size bin): TBD
- Reporting rule for negative and null results: TBD
