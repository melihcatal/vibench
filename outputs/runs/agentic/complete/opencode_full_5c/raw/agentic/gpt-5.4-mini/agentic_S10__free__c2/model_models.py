from dataclasses import dataclass
from typing import Any


@dataclass
class TextRequest:
    text: str
    model: str | None = None


@dataclass
class QARequest:
    question: str
    context: str
    model: str | None = None


@dataclass
class StructuredOutput:
    data: dict[str, Any]


def normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()


def normalize_json_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"value": payload}
