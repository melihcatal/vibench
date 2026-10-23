from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class LLMRequest:
    prompt: str
    model: str = "gemini-pro"
    max_tokens: int = 100
    temperature: float = 0.7


@dataclass
class LLMResponse:
    text: str
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None


@dataclass
class ContextualQuestionRequest:
    question: str
    context: str
    model: str = "gemini-pro"
    max_tokens: int = 200
    temperature: float = 0.7


@dataclass
class JsonExtractionRequest:
    text: str
    schema: Dict[str, Any]
    model: str = "gemini-pro"
    max_tokens: int = 500
    temperature: float = 0.3


@dataclass
class SafetyCheckRequest:
    text: str


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "embedding-001"


@dataclass
class SpokenBriefRequest:
    text: str
    voice_name: str = "en-US-Standard-C"
