from typing import List, Dict, Any, Literal, TypedDict


class TranslationPayload(TypedDict):
    text: str
    source_language: str
    target_language: str


class BatchTranslationPayload(TypedDict):
    texts: List[str]
    source_language: str
    target_language: str


class MarkupTranslationPayload(TypedDict):
    content: str
    source_language: str
    target_language: str
    markup_format: Literal["HTML", "XML"]


class DictionaryTranslationPayload(TypedDict):
    data: Dict[str, str]
    source_language: str
    target_language: str


class QualitySummaryPayload(TypedDict):
    translated_text: str
    source_text: str
    language: str


class UnsafeCopyCheckPayload(TypedDict):
    text: str
    language: str


class TranslationMemoryEmbeddingPayload(TypedDict):
    segment: str
    language: str


class LocalizedAudioPreviewPayload(TypedDict):
    text: str
    language: str
    voice_id: str
