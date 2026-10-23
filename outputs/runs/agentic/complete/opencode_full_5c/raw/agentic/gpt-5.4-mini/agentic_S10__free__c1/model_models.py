from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextRequest:
    text: str
    model: Optional[str] = None


@dataclass
class QARequest:
    question: str
    context: str
    model: Optional[str] = None


@dataclass
class JSONExtractionRequest:
    text: str
    schema_hint: str
    model: Optional[str] = None


@dataclass
class GeneratedTextResponse:
    text: str
    raw: Any


@dataclass
class JSONExtractionResponse:
    data: Dict[str, Any]
    raw: Any


def normalize_output_text(text: str) -> str:
    return text.strip()
