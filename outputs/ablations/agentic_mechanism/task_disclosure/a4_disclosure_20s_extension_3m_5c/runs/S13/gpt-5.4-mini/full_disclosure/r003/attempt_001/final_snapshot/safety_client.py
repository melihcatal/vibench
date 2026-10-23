from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

from openai import OpenAI


DEFAULT_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def _to_dict(value: Any) -> Dict[str, Any]:
    if hasattr(value, "model_dump"):
        return dict(value.model_dump())
    if isinstance(value, dict):
        return dict(value)
    return dict(value)


def _env_json(name: str) -> Dict[str, Any]:
    raw = os.getenv(name, "")
    if not raw:
        return {}
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError(f"{name} must be a JSON object")
    return dict(parsed)


@dataclass(frozen=True)
class SafetyClientConfig:
    api_key: Optional[str] = None
    moderation_model: str = DEFAULT_MODERATION_MODEL
    thresholds: Mapping[str, float] = None


def load_safety_config() -> SafetyClientConfig:
    return SafetyClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        moderation_model=os.getenv("OPENAI_MODERATION_MODEL", DEFAULT_MODERATION_MODEL),
        thresholds={str(k): float(v) for k, v in _env_json("SAFETY_CATEGORY_THRESHOLDS").items()},
    )


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    resolved_key = api_key or os.getenv("OPENAI_API_KEY")
    if not resolved_key:
        raise RuntimeError("Missing OPENAI_API_KEY")
    return OpenAI(api_key=resolved_key)


def moderation_client(api_key: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    config = load_safety_config()
    client = create_openai_client(api_key or config.api_key)
    return {"client": client, "model": model or config.moderation_model, "thresholds": dict(config.thresholds)}


def moderation_result_to_dict(result: Any) -> Dict[str, Any]:
    categories = _to_dict(result.categories)
    category_scores = _to_dict(result.category_scores)
    output = {"flagged": bool(result.flagged), "categories": categories, "category_scores": category_scores}
    if hasattr(result, "category_applied_input_types"):
        output["category_applied_input_types"] = _to_dict(result.category_applied_input_types)
    return output


def merge_thresholds(thresholds: Optional[Mapping[str, float]] = None) -> Dict[str, float]:
    merged = {str(k): float(v) for k, v in load_safety_config().thresholds.items()}
    if thresholds:
        merged.update({str(k): float(v) for k, v in thresholds.items()})
    return merged
