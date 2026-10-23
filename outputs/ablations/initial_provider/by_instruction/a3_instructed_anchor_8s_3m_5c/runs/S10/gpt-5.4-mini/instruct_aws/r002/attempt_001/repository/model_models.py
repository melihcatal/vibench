from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ChatRequest:
    system: str
    user: str
    max_tokens: int = 512
    temperature: float = 0.2


@dataclass
class ChatResponse:
    text: str
    raw: Dict[str, Any]


@dataclass
class StreamChunk:
    text: str
    raw: Dict[str, Any]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(normalize_text(item) for item in value)
    if isinstance(value, dict):
        for key in ("text", "content", "outputText", "completion"):
            if key in value:
                return normalize_text(value[key])
    return str(value)


def extract_json_like(text: str) -> Dict[str, Any]:
    import json
    import re

    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return {"text": text}
    try:
        return json.loads(match.group(0))
    except Exception:
        return {"text": text}
