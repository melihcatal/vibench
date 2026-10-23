from typing import List, Dict, Any

class TranslationRequest:
    text: str
    source_language: str
    target_language: str

class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str

class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str

class BatchTranslationResponse:
    translated_texts: List[str]
    source_language: str
    target_language: str

class DictionaryTranslationRequest:
    data: Dict[str, str]
    source_language: str
    target_language: str

class DictionaryTranslationResponse:
    translated_data: Dict[str, str]
    source_language: str
    target_language: str
