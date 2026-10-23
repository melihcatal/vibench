from dataclasses import dataclass
from typing import List


@dataclass
class EmbeddingResponse:
    embedding: List[float]


@dataclass
class EmbeddingBatchResponse:
    embeddings: List[List[float]]


@dataclass
class SummaryRequest:
    text_to_summarize: str


@dataclass
class SummaryResponse:
    summary: str


@dataclass
class ContentSafetyRequest:
    text: str


@dataclass
class ContentSafetyResponse:
    is_safe: bool
    moderation_results: dict


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: str = "auto"


@dataclass
class TranslationResponse:
    translated_text: str


@dataclass
class AudioBriefRequest:
    text: str
    voice_name: str = "en-US-Standard-C"
    language_code: str = "en-US"


@dataclass
class AudioBriefResponse:
    audio_content: bytes
