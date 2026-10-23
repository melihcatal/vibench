#!/usr/bin/env python3
"""Single source of truth for study-model metadata.

Backed by benchmark/vibench/models.json. Evaluation, table, and plotting
scripts derive the control baseline, study membership, canonical table
order, ecosystems, tiers, and default display names from here instead of
hard-coding model lists. Per-artifact label dictionaries (LaTeX vs. chart
vs. compact styles) may shadow ``display_name`` but should fall back to it
so newly registered models render without further script changes.

Study membership and order come from the ``study_order`` field: models
carrying it form the current study grid, sorted ascending. Models without
``study_order`` (legacy routes, local variants, candidate additions) are
still resolvable through ``models_info``/``display_name`` but never enter
baselines or table order implicitly.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
MODELS_JSON = BASE_DIR / "benchmark" / "vibench" / "models.json"


@lru_cache(maxsize=1)
def _entries() -> tuple[dict, ...]:
    with open(MODELS_JSON) as f:
        data = json.load(f)
    return tuple(data["models"])


def models_info() -> dict[str, dict]:
    """All models.json entries keyed by model id."""
    return {m["id"]: m for m in _entries()}


def _study_entries() -> list[dict]:
    entries = [m for m in _entries() if m.get("study_order") is not None]
    if not entries:
        raise RuntimeError(
            f"No models with a 'study_order' field in {MODELS_JSON} — the file "
            "is stale or was replaced by a copy without registry metadata. "
            "Refusing to run with an empty study set/control baseline."
        )
    return sorted(entries, key=lambda m: m["study_order"])


def study_models() -> list[str]:
    """All models of the current study, in canonical table order."""
    return [m["id"] for m in _study_entries()]


def strict_controls() -> list[str]:
    """The non-affiliated control baseline, in canonical order."""
    return [m["id"] for m in _study_entries() if m.get("role") == "control"]


def affiliated_models() -> list[str]:
    """Affiliated study models, in canonical table order."""
    return [m["id"] for m in _study_entries() if m.get("role") == "affiliated"]


def role(model_id: str) -> str | None:
    """'affiliated', 'control', or 'independent' (None if unknown)."""
    return models_info().get(model_id, {}).get("role")


def ecosystem(model_id: str) -> str | None:
    return models_info().get(model_id, {}).get("ecosystem_affiliation")


def tier(model_id: str) -> str | None:
    """'flagship' or 'budget' (None if unknown)."""
    return models_info().get(model_id, {}).get("tier")


def display_name(model_id: str) -> str:
    """Default display name; falls back to the raw model id."""
    return models_info().get(model_id, {}).get("display_name") or model_id
