#!/usr/bin/env python3
"""Compatibility wrapper for the downstream-leakage figure script."""

from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
runpy.run_path(
    str(ROOT / "paper" / "figures" / "appendix" / "downstream_leakage" / "plot.py"),
    run_name="__main__",
)
