from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextRequest:
    text: str
    model: Optional[str] = None


@dataclass
class ContextQuestionRequest:
    context: str
    question: str
    model: Optional[str] = None


@dataclass
class ResultText:
    text: str
    raw: Any = None


def build_prompt(prefix: str, body: str) -> str:
    return f"{prefix}\n\n{body}".strip()


def as_dict(data: Any) -> Dict[str, Any]:
    if isinstance(data, dict):
        return data
    return {"value": data}
