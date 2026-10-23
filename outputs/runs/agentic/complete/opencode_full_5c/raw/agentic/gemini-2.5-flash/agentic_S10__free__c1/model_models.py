from dataclasses import dataclass
from typing import List, Dict, Any, Literal, Optional


@dataclass
class LLMRequest:
    prompt: str
    model_family: Literal[
        "gemini-pro", "gemini-1.5-pro-latest", "gemini-1.5-flash-latest"
    ]
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    context: Optional[str] = None
    json_schema: Optional[Dict[str, Any]] = None


@dataclass
class LLMResponse:
    text: str
    metadata: Dict[str, Any]


@dataclass
class LLMStreamResponse:
    chunk: str
    metadata: Dict[str, Any]


@dataclass
class EmbeddingRequest:
    text: str
    model_family: Literal["embedding-001", "text-embedding-004"]


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    metadata: Dict[str, Any]


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str
    metadata: Dict[str, Any]


@dataclass
class TextToSpeechRequest:
    text: str
    language_code: str
    voice_name: Optional[str] = None


@dataclass
class TextToSpeechResponse:
    audio_content: bytes
    metadata: Dict[str, Any]


@dataclass
class SafetyCheckRequest:
    text: str
    threshold: Literal[
        "BLOCK_NONE", "BLOCK_LOW_AND_ABOVE", "BLOCK_MED_AND_ABOVE", "BLOCK_ONLY_HIGH"
    ]


@dataclass
class SafetyCheckResponse:
    is_safe: bool
    safety_ratings: List[Dict[str, Any]]
