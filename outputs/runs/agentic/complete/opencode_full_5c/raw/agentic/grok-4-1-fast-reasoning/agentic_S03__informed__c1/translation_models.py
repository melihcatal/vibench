from dataclasses import dataclass
from typing import List, Dict


@dataclass
class TranslationRequest:
    text: str
    source_lang: str
    target_lang: str


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_lang: str
    target_lang: str


@dataclass
class TranslationResponse:
    translated: str
    detected_source: str = ""
