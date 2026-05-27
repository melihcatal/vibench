#!/usr/bin/env python3
"""Compatibility wrapper for the prompt-format figure script."""

from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
runpy.run_path(
    str(ROOT / "paper" / "figures" / "appendix" / "prompt_format" / "plot.py"),
    run_name="__main__",
)
