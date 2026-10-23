from typing import List, Dict, Optional, TypedDict

class TranslationRequest(TypedDict):
    text: str
    target_language: str
    source_language: Optional[str]

class TranslationResponse(TypedDict):
    translated_text: str
    detected_source_language: Optional[str]

class BatchTranslationRequest(TypedDict):
    texts: List[str]
    target_language: str
    source_language: Optional[str]

class BatchTranslationResponse(TypedDict):
    translated_texts: List[str]
    detected_source_languages: List[Optional[str]]

class DictionaryTranslationRequest(TypedDict):
    data: Dict[str, str]
    target_language: str
    source_language: Optional[str]

class DictionaryTranslationResponse(TypedDict):
    translated_data: Dict[str, str]
