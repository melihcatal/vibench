#!/usr/bin/env python3
"""Compatibility wrapper for result figures now stored with the figure assets."""

from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
runpy.run_path(str(ROOT / "paper" / "figures" / "results" / "plot_all.py"), run_name="__main__")
