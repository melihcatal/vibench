from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ChatRequest:
    prompt: str
    model: str = "gemini-pro"
    temperature: float = 0.7
    max_output_tokens: int = 1024


@dataclass
class ChatResponse:
    text: str
    finish_reason: Optional[str] = None


@dataclass
class Message:
    role: str
    parts: List[Dict[str, Any]]


@dataclass
class ContentSafetyRequest:
    text: str


@dataclass
class ContentSafetyResponse:
    is_safe: bool
    moderation_results: Optional[List[Dict[str, Any]]] = None


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "embedding-001"


@dataclass
class EmbeddingResponse:
    embedding: List[float]


@dataclass
class TextToSpeechRequest:
    text: str
    voice_name: str = "en-US-Wavenet-D"
    language_code: str = "en-US"


@dataclass
class TextToSpeechResponse:
    audio_content: bytes
