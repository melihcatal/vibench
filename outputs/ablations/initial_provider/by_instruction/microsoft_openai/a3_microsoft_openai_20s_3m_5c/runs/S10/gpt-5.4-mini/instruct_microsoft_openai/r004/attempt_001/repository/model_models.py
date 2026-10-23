from dataclasses import dataclass
from typing import Any


@dataclass
class TextRequest:
    text: str
    prompt: str | None = None
    context: str | None = None
    language: str | None = None


@dataclass
class TextResponse:
    text: str
    model: str | None = None
    usage: dict[str, Any] | None = None


def normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()


def json_prompt(text: str) -> str:
    return f"Extract valid JSON from the following text and return only JSON:\n{text}"


def safe_context_prompt(question: str, context: str) -> str:
    return f"Answer the question using only the context.\nQuestion: {question}\nContext: {context}"
