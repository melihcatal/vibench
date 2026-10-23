from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LLMRequest:
    prompt: str
    model: str = "gemini-pro"
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    safety_settings: Optional[List[Dict[str, Any]]] = None


@dataclass
class LLMResponse:
    text: str
    usage_metadata: Optional[Dict[str, Any]] = None
    finish_reason: Optional[str] = None


@dataclass
class SafetyRequest:
    text: str


@dataclass
class SafetyResponse:
    is_safe: bool
    categories: Dict[str, str]


@dataclass
class TranslateRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None


@dataclass
class TranslateResponse:
    translated_text: str
    detected_language_code: Optional[str] = None


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "models/embedding-001"


@dataclass
class EmbeddingResponse:
    embedding: List[float]


@dataclass
class TextToSpeechRequest:
    text: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Neural2-C"
    audio_encoding: str = "MP3"


@dataclass
class TextToSpeechResponse:
    audio_content: bytes
