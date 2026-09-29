import random

import numpy as np
import pytest
import torch

from src.utils.config import config_hash, load_config
from src.utils.logger import CSVLogger
from src.utils.seed import seed_everything


def _draw():
    # The legacy global NumPy RNG is what seed_everything seeds, so it is what we check.
    np_draw = float(np.random.rand())  # noqa: NPY002
    return random.random(), np_draw, float(torch.rand(1))


def test_seed_reproducible():
    seed_everything(7)
    a = _draw()
    seed_everything(7)
    b = _draw()
    assert a == b


def test_seed_differs_across_seeds():
    seed_everything(1)
    a = _draw()
    seed_everything(2)
    assert a != _draw()


def test_seed_rejects_invalid():
    with pytest.raises(ValueError):
        seed_everything(-1)


def test_config_hash_order_invariant():
    assert config_hash({"a": 1, "b": {"c": 2, "d": 3}}) == config_hash(
        {"b": {"d": 3, "c": 2}, "a": 1}
    )
    assert config_hash({"a": 1}) != config_hash({"a": 2})


def test_load_config(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text("lr: 0.001\nmodel: gps\n", encoding="utf-8")
    assert load_config(p) == {"lr": 0.001, "model": "gps"}
    bad = tmp_path / "bad.yaml"
    bad.write_text("- 1\n- 2\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_config(bad)


def test_csv_logger(tmp_path):
    log = CSVLogger(tmp_path / "out" / "r.csv")
    log.log({"seed": 0, "f1": 0.5})
    log.log({"seed": 1, "f1": 0.6})
    with pytest.raises(ValueError):
        log.log({"seed": 2})
    # Reopening keeps the header and appends.
    CSVLogger(tmp_path / "out" / "r.csv").log({"seed": 3, "f1": 0.7})
    lines = (tmp_path / "out" / "r.csv").read_text().strip().splitlines()
    assert lines[0] == "seed,f1" and len(lines) == 4
