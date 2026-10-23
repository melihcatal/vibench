from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextRequest:
    text: str
    instruction: Optional[str] = None


@dataclass
class QuestionRequest:
    question: str
    context: str


@dataclass
class JsonExtractionRequest:
    text: str
    schema_hint: Optional[str] = None


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_json_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"value": payload}
