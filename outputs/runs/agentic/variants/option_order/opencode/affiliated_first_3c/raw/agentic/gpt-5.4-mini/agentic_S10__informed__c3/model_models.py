from dataclasses import dataclass
from typing import Any


@dataclass
class TextRequest:
    text: str
    model: str


@dataclass
class QuestionContextRequest:
    question: str
    context: str
    model: str


@dataclass
class StructuredResult:
    content: str
    data: Any | None = None


def normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()
