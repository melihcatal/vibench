from typing import TypedDict


class StreamingTranscript(TypedDict):
    text: str
    is_final: bool


class TranslationResponse(TypedDict):
    translated_text: str
    detected_language_code: str


class SafetyRating(TypedDict):
    attribute: str
    score: float


class SummaryResponse(TypedDict):
    summary: str


class EmbeddingResponse(TypedDict):
    embeddings: list[list[float]]
