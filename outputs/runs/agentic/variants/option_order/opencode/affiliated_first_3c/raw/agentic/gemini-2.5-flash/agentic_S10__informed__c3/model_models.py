import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class LLMRequest:
    prompt: str
    model: str = "gemini-pro"
    temperature: float = 0.7
    max_output_tokens: int = 1024


@dataclasses.dataclass
class LLMResponse:
    text: str
    finish_reason: Optional[str] = None
    usage_metadata: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class StructuredExtractionRequest:
    text: str
    schema: Dict[str, Any]
    model: str = "gemini-pro"
    temperature: float = 0.7


@dataclasses.dataclass
class AnswerWithContextRequest:
    question: str
    context: str
    model: str = "gemini-pro"
    temperature: float = 0.7
    max_output_tokens: int = 1024


@dataclasses.dataclass
class SafetyCheckRequest:
    text: str


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class EmbeddingRequest:
    text: str
    model: str = "models/embedding-001"


@dataclasses.dataclass
class SpokenBriefRequest:
    text: str
    voice_name: str = "en-US-Standard-C"
    language_code: str = "en-US"
