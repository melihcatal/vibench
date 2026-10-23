from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PromptRequest:
    prompt: str
    temperature: float = 0.2
    max_output_tokens: int = 512


@dataclass
class PlatformModelResponse:
    text: str
    model: str
    usage: Optional[Dict[str, Any]] = None
    resource_name: Optional[str] = None
    raw_response: Optional[Any] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, Iterable):
        return " ".join(str(v).strip() for v in value if str(v).strip())
    return str(value).strip()


def merge_usage(*items: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for item in items:
        if not item:
            continue
        for key, value in item.items():
            if isinstance(value, (int, float)) and key in merged and isinstance(merged[key], (int, float)):
                merged[key] += value
            else:
                merged[key] = value
    return merged
