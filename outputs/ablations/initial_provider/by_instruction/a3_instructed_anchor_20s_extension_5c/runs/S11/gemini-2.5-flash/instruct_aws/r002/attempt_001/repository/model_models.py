from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class ModelInvocationRequest:
    prompt: str
    model_id: str
    max_tokens: int = 50
    temperature: float = 0.7

@dataclass
class ModelInvocationResponse:
    generated_text: str
    model_id: str

@dataclass
class ModelStreamResponse:
    chunk_text: str
    raw_provider_response: Dict[str, Any] # To preserve the raw provider chunk

@dataclass
class ModelMetadataResponse:
    generated_text: str
    metadata: Dict[str, Any]

@dataclass
class SafetyCheckRequest:
    text: str

@dataclass
class SafetyCheckResponse:
    is_safe: bool
    safety_scores: Dict[str, float] = field(default_factory=dict)
    provider_response: Optional[Dict[str, Any]] = None

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    provider_response: Optional[Dict[str, Any]] = None

@dataclass
class EmbeddingRequest:
    text: str
    model_id: str

@dataclass
class EmbeddingResponse:
    embedding: list[float]
    model_id: str
    provider_response: Optional[Dict[str, Any]] = None

@dataclass
class AudioBriefingRequest:
    text: str
    voice_id: str
    language_code: str = "en-US"

@dataclass
class AudioBriefingResponse:
    audio_content: bytes
    provider_response: Optional[Dict[str, Any]] = None
