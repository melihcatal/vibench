import dataclasses
from typing import Dict, Any, List, Optional


@dataclasses.dataclass
class ChatRequest:
    model: str
    prompt: str
    temperature: float = 0.7
    max_output_tokens: int = 2048


@dataclasses.dataclass
class ChatResponse:
    text: str
    finish_reason: Optional[str] = None


@dataclasses.dataclass
class Message:
    role: str
    parts: List[Dict[str, Any]]


@dataclasses.dataclass
class HarmCategory:
    category: str
    threshold: str


@dataclasses.dataclass
class ContentSafetyRequest:
    text: str
    categories: Optional[List[str]] = None


@dataclasses.dataclass
class ContentSafetyResponse:
    is_safe: bool
    detection_results: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str


@dataclasses.dataclass
class EmbeddingRequest:
    text: str
    model: str


@dataclasses.dataclass
class EmbeddingResponse:
    embedding: List[float]


@dataclasses.dataclass
class TextToSpeechRequest:
    text: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Standard-A"
    audio_encoding: str = "MP3"


@dataclasses.dataclass
class TextToSpeechResponse:
    audio_content: bytes
