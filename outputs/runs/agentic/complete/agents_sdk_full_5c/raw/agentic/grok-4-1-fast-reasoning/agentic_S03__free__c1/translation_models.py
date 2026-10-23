from typing import TypedDict, List, Optional, Union

class TranslateRequest(TypedDict):
    text: str
    source_lang: str
    target_lang: str

class BatchTranslateRequest(TypedDict):
    texts: List[str]
    source_lang: str
    target_lang: str

class TranslationResult(TypedDict):
    translated_text: str
    detected_lang: Optional[str]
    confidence: Optional[float]

class QualitySummaryRequest(TypedDict):
    original: str
    translated: str
    source_lang: str
    target_lang: str