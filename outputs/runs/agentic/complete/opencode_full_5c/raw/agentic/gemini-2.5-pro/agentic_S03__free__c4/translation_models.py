from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class TranslationRequest:
    content: str
    target_language: str
    source_language: str


@dataclass
class BatchTranslationRequest:
    content: List[str]
    target_language: str
    source_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: str


@dataclass
class BatchTranslationResponse:
    translations: List[Dict[str, Any]]
