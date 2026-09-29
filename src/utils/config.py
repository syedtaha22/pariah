"""
YAML config loading and stable config hashing.
"""

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """
    Load a YAML config file into a dict.
    """
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise ValueError(f"Config {path} must contain a mapping at the top level")
    return cfg


def config_hash(cfg: dict[str, Any], length: int = 12) -> str:
    """
    Return a short hash that is stable across key order and process runs.
    """
    canonical = json.dumps(cfg, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:length]
