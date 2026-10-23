from dataclasses import dataclass
from typing import List


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    model: str


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str
    model: str


@dataclass
class TranslationResponse:
    text: str


def normalize_text(text: str) -> str:
    return " ".join(text.split()) if text is not None else ""
