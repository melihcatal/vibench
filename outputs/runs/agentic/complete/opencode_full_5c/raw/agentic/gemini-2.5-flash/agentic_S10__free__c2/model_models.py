from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TextGenerationRequest:
    prompt: str
    temperature: float = 0.7
    max_output_tokens: int = 256


@dataclass
class TextGenerationResponse:
    summary: str


@dataclass
class JsonExtractionRequest:
    text: str
    json_schema: str


@dataclass
class JsonExtractionResponse:
    extracted_json: str


@dataclass
class QuestionAnsweringRequest:
    question: str
    context: str


@dataclass
class QuestionAnsweringResponse:
    answer: str


@dataclass
class StreamCompletionRequest:
    prompt: str
    temperature: float = 0.7
    max_output_tokens: int = 256


@dataclass
class StreamCompletionChunk:
    text: str


@dataclass
class SafetyCheckRequest:
    text: str


@dataclass
class SafetyCheckResponse:
    is_safe: bool
    safety_attributes: dict


@dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str


@dataclass
class EmbeddingRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]


@dataclass
class SpokenBriefRequest:
    text: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Neural2-C"


@dataclass
class SpokenBriefResponse:
    audio_content: bytes
