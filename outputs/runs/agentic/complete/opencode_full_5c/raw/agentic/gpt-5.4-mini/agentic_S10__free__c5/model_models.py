from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TextRequest:
    text: str
    context: Optional[str] = None
    question: Optional[str] = None
    target_language: Optional[str] = None


@dataclass
class TextResponse:
    text: str
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("text", "output_text", "content"):
            if key in value and isinstance(value[key], str):
                return value[key].strip()
    return str(value).strip()


def normalize_json_text(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {"text": normalize_text(value)}


def normalize_embedding(values: List[float]) -> List[float]:
    return [float(v) for v in values]
