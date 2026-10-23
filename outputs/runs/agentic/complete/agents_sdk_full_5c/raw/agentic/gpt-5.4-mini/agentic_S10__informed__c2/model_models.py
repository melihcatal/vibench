from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class ChatRequest:
    prompt: str
    model: str
    system: Optional[str] = None
    temperature: float = 0.2


@dataclass
class ChatResponse:
    text: str
    model: str
    raw: Any


@dataclass
class JsonExtraction:
    data: Dict[str, Any]
    model: str


@dataclass
class SafetyResult:
    unsafe: bool
    score: float
    raw: Any


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class EmbeddingResult:
    vectors: List[List[float]]
    model: str


@dataclass
class SpeechBrief:
    text: str
    audio_path: Optional[str] = None


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
