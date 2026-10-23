from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TextInput:
    text: str


@dataclass
class ContextQuestion:
    context: str
    question: str


@dataclass
class StructuredJsonRequest:
    text: str
    schema_hint: Optional[str] = None


@dataclass
class GenerationResult:
    text: str
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_json_output(value: str) -> str:
    return normalize_text(value)
