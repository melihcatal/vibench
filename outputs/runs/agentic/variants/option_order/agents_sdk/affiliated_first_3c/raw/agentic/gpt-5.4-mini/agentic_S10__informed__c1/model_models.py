from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class LLMRequest:
    prompt: str
    system: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 512


@dataclass
class LLMResponse:
    text: str
    model: str
    raw: Any = None


@dataclass
class JsonExtraction:
    data: Dict[str, Any]
    model: str


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: List[str] = []
        for item in value:
            if isinstance(item, dict) and "text" in item:
                parts.append(str(item["text"]))
            else:
                parts.append(str(item))
        return "".join(parts)
    return str(value)


def parse_json_object(text: str) -> Dict[str, Any]:
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = candidate.strip("`")
    return json.loads(candidate)
