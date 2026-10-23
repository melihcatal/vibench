from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class GenerationRequest:
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.2
    locale: str = "en"

    def to_chat_messages(self) -> List[Dict[str, str]]:
        return [{"role": "user", "content": self.prompt}]


@dataclass
class PlatformResource:
    deployment_name: str
    azure_deployment: str
    model_family: str


@dataclass
class GenerationResult:
    text: str
    model: str
    usage: Dict[str, Any]
    resource: Dict[str, Any]
    raw_response: Any


@dataclass
class SafetyResult:
    safe: bool
    scores: Dict[str, float]
    raw_response: Any


@dataclass
class TranslationResult:
    text: str
    target_locale: str
    detected_language: Optional[str]
    raw_response: Any


@dataclass
class EmbeddingResult:
    vector: List[float]
    model: str
    dimensions: int
    raw_response: Any


@dataclass
class AudioBriefResult:
    audio_bytes: bytes
    content_type: str
    raw_response: Any


def usage_to_dict(usage: Any) -> Dict[str, Any]:
    if usage is None:
        return {}
    if hasattr(usage, "model_dump"):
        return usage.model_dump()
    if isinstance(usage, dict):
        return usage
    return {
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
    }


def first_text_from_chat_response(response: Any) -> str:
    choices = getattr(response, "choices", None) or response.get("choices", [])
    if not choices:
        return ""
    first = choices[0]
    message = getattr(first, "message", None) or first.get("message", {})
    if isinstance(message, dict):
        return message.get("content", "") or ""
    return getattr(message, "content", "") or ""


def chunk_delta_text(chunk: Any) -> str:
    choices = getattr(chunk, "choices", None) or chunk.get("choices", [])
    if not choices:
        return ""
    delta = getattr(choices[0], "delta", None) or choices[0].get("delta", {})
    if isinstance(delta, dict):
        return delta.get("content", "") or ""
    return getattr(delta, "content", "") or ""
