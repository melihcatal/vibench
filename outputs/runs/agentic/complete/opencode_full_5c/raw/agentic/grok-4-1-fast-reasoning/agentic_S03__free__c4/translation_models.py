from typing import TypedDict, List, Optional, Dict, Any


class TranslationRequest(TypedDict):
    text: str
    source_lang: Optional[str]
    target_lang: str


class BatchTranslationRequest(TypedDict):
    texts: List[str]
    source_lang: Optional[str]
    target_lang: str


class TranslationResult(TypedDict):
    translated_text: str
    detected_source_lang: str
    target_lang: str
