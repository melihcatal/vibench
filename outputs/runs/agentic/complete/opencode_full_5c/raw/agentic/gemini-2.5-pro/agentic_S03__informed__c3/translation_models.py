from typing import TypedDict


class TranslationRequest(TypedDict):
    text: str
    target_language: str
    source_language: str


class BatchTranslationRequest(TypedDict):
    texts: list[str]
    target_language: str
    source_language: str


class TranslationResponse(TypedDict):
    translated_text: str
    detected_source_language: str


class BatchTranslationResponse(TypedDict):
    translations: list[TranslationResponse]
