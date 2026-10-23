from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class GenerationRequest:
    text: Optional[str] = None
    prompt: Optional[str] = None
    question: Optional[str] = None
    context: Optional[str] = None
    system_prompt: Optional[str] = None
    max_output_tokens: int = 512
    temperature: float = 0.2
    top_p: float = 0.95
    model: Optional[str] = None


@dataclass
class GenerationResult:
    provider: str
    model: str
    text: str
    usage: Dict[str, Any] = field(default_factory=dict)
    finish_reason: Optional[str] = None


@dataclass
class SafetyResult:
    provider: str
    flagged: bool
    scores: Dict[str, float]
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    detected_source_language: Optional[str] = None
    target_language: Optional[str] = None


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embedding: List[float]
    dimensions: int


@dataclass
class SpeechResult:
    provider: str
    audio_bytes: bytes
    content_type: str
    voice: Optional[str] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def compact_text_parts(*parts: Any) -> str:
    cleaned = [normalize_text(part) for part in parts]
    return "\n\n".join(part for part in cleaned if part)


def usage_to_dict(usage: Any) -> Dict[str, Any]:
    if usage is None:
        return {}
    if isinstance(usage, dict):
        return usage
    if hasattr(usage, "model_dump"):
        return usage.model_dump()
    if hasattr(usage, "dict"):
        return usage.dict()
    return {
        key: getattr(usage, key)
        for key in dir(usage)
        if not key.startswith("_") and not callable(getattr(usage, key))
    }


def ensure_json_schema_name(name: str) -> str:
    safe = "".join(ch if ch.isalnum() else "_" for ch in normalize_text(name))
    return safe or "structured_output"
