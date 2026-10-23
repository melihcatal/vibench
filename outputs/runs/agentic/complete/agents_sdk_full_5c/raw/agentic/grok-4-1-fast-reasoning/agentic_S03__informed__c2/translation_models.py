from dataclasses import dataclass
from typing import List, Dict, Any

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
    translated_text: str

@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]