"""
Global seeding and determinism controls.
"""

import os
import random

import numpy as np
import torch


def seed_everything(seed: int, deterministic: bool = True) -> None:
    """
    Seed Python, NumPy and PyTorch (CPU and CUDA).

    With ``deterministic=True`` cuDNN autotuning is disabled and PyTorch is asked to use
    deterministic algorithms (warning instead of failing when none exists), so that runs
    with the same seed and config are comparable.
    """
    if not isinstance(seed, int) or seed < 0:
        raise ValueError(f"seed must be a non-negative int, got {seed!r}")
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)  # noqa: NPY002 (legacy global RNG is seeded on purpose for third-party code)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    if deterministic:
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        torch.use_deterministic_algorithms(True, warn_only=True)
