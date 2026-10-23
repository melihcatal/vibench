from typing import List, Dict
from dataclasses import dataclass

@dataclass
class TranslationRequest:
    source_language_code: str
    target_language_code: str
    content: str

@dataclass
class SingleTranslationResponse:
    translated_text: str
    detected_language_code: str

@dataclass
class BatchTranslationRequest:
    source_language_code: str
    target_language_code: str
    content: List[str]

@dataclass
class BatchTranslationResponse:
    translations: List[SingleTranslationResponse]

@dataclass
class DictionaryTranslationRequest:
    source_language_code: str
    target_language_code: str
    content: Dict[str, str]

@dataclass
class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, str]
