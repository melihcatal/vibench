from typing import List, Dict, Any

class TranslationRequest:
    text: str
    source_language: str
    target_language: str

class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str

class DictionaryTranslationRequest:
    dictionary: Dict[str, str]
    source_language: str
    target_language: str

class TranslationResponse:
    text: str
    source_language: str
    target_language: str

class BatchTranslationResponse:
    translated_texts: List[str]
    source_language: str
    target_language: str

class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, str]
    source_language: str
    target_language: str
