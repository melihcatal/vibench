import os
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI

from safety_models import BatchModerationResult, ModerationResult, normalize_messages


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_threshold_env(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except Exception:
        return default


def parse_moderation_response(payload: Dict[str, Any]) -> ModerationResult:
    return ModerationResult.from_dict(payload)


def parse_batch_moderation_response(
    items: Iterable[Dict[str, Any]],
) -> BatchModerationResult:
    return BatchModerationResult(
        results=[ModerationResult.from_dict(item) for item in items]
    )


def normalize_text_input(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return str(value.get("text") or value.get("content") or "")
    return str(value)


def normalize_batch_input(values: Iterable[Any]) -> List[str]:
    return normalize_messages(values)
