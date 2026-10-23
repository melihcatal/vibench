from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TextRequest:
    text: str
    model: Optional[str] = None


@dataclass
class ContextQARequest:
    question: str
    context: str
    model: Optional[str] = None


@dataclass
class JsonExtractionRequest:
    text: str
    schema_hint: str
    model: Optional[str] = None


@dataclass
class TextResponse:
    text: str
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_json_candidate(text: str) -> Dict[str, Any]:
    import json

    cleaned = text.strip().strip("`")
    if cleaned.startswith("json"):
        cleaned = cleaned[4:].strip()
    return json.loads(cleaned)


def normalize_list(items: List[Any]) -> List[str]:
    return [normalize_text(item) for item in items if normalize_text(item)]
