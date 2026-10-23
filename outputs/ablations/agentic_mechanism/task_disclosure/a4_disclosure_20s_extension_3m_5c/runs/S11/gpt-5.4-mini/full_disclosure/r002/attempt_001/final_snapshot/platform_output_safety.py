from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional

from openai import OpenAI

from model_client import load_managed_model_platform_config


@dataclass(frozen=True)
class PlatformSafetyResult:
    unsafe: bool
    categories: dict[str, bool] = field(default_factory=dict)
    scores: dict[str, float] = field(default_factory=dict)
    raw_response: Any = None
    provider: str = "openai"


def _extract_categories(payload: Any) -> dict[str, bool]:
    if isinstance(payload, Mapping):
        return {str(k): bool(v) for k, v in payload.items()}
    return {}


def _extract_scores(payload: Any) -> dict[str, float]:
    if isinstance(payload, Mapping):
        result: dict[str, float] = {}
        for key, value in payload.items():
            try:
                result[str(key)] = float(value)
            except (TypeError, ValueError):
                continue
        return result
    return {}


def check_platform_output_safety(
    output_text: str,
    *,
    model: Optional[str] = None,
    env: Optional[Mapping[str, str]] = None,
) -> PlatformSafetyResult:
    source = env if env is not None else os.environ
    config = load_managed_model_platform_config(source)
    client = OpenAI(
        api_key=config.api_key,
        base_url=config.base_url,
        organization=config.organization,
        project=config.project,
    )
    response = client.moderations.create(
        model=model or "omni-moderation-latest",
        input=output_text,
    )
    result = response.results[0]
    categories = _extract_categories(getattr(result, "categories", None) or {})
    scores = _extract_scores(getattr(result, "category_scores", None) or {})
    unsafe = bool(getattr(result, "flagged", False)) or any(categories.values())
    return PlatformSafetyResult(
        unsafe=unsafe,
        categories=categories,
        scores=scores,
        raw_response=response,
    )
