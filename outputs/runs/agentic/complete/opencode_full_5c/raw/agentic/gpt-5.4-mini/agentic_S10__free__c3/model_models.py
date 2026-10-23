from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextRequest:
    text: str
    model: Optional[str] = None


@dataclass
class QuestionRequest:
    question: str
    context: str
    model: Optional[str] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_json_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return {str(k): v for k, v in data.items()}
