from dataclasses import dataclass
from typing import List, Optional, Any


@dataclass
class PlatformModelRequest:
    prompt: str
    model_id: str


@dataclass
class PlatformModelResponse:
    text: str
    raw_response: Optional[Any] = None


@dataclass
class PlatformModelStreamChunk:
    text: str
    raw_chunk: Optional[Any] = None


@dataclass
class PlatformModelMetadata:
    input_token_count: int
    output_token_count: int
    raw_metadata: Optional[Any] = None


@dataclass
class SafetyResult:
    is_safe: bool
    raw_result: Optional[Any] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    raw_result: Optional[Any] = None


@dataclass
class EmbeddingResult:
    embeddings: List[List[float]]
    raw_result: Optional[Any] = None


@dataclass
class AudioResult:
    output_path: str
    raw_result: Optional[Any] = None
