from dataclasses import dataclass, asdict
from typing import Any
import json


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
class ModelResponse:
    text: str
    raw: Any | None = None


def parse_json_object(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except Exception:
        return {"text": text}


def to_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return dict(value)
