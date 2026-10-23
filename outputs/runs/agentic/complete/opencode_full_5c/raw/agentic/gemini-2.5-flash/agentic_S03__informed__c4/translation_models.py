from typing import List, Dict, Any, Literal, Optional


class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None
    mime_type: Literal["text/plain", "text/html"] = "text/plain"


class BatchTranslationRequest:
    texts: List[str]
    target_language_code: str
    source_language_code: Optional[str] = None
    mime_type: Literal["text/plain", "text/html"] = "text/plain"


class DictionaryTranslationRequest:
    data: Dict[str, str]
    target_language_code: str
    source_language_code: Optional[str] = None


class TranslationResponse:
    translated_text: str
    detected_source_language_code: Optional[str] = None


class BatchTranslationResponse:
    translations: List[str]
    detected_source_language_codes: List[Optional[str]]
