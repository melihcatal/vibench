from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


class ModelRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    role: ModelRole
    content: str


@dataclass
class PlatformModelRequest:
    model: str
    messages: List[Message]
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    stop: Optional[List[str]] = None
    stream: bool = False
    seed: Optional[int] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class PlatformModelResponse:
    content: str
    model: str
    finish_reason: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    request_id: Optional[str] = None
    raw_response: Optional[Any] = None


@dataclass
class StreamChunk:
    delta: str
    finish_reason: Optional[str] = None
    index: int = 0


@dataclass
class PlatformStreamResponse:
    content: str
    model: str
    chunks: List[StreamChunk] = field(default_factory=list)
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    request_id: Optional[str] = None
    raw_response: Optional[Any] = None


@dataclass
class PlatformMetadataResponse:
    content: str
    model: str
    model_id: str
    organization_id: Optional[str] = None
    request_id: Optional[str] = None
    system_fingerprint: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    created_timestamp: Optional[int] = None
    raw_response: Optional[Any] = None


@dataclass
class SafetyViolation:
    category: str
    severity: str
    score: float
    flagged: bool


@dataclass
class SafetyCheckResult:
    flagged: bool
    violations: List[SafetyViolation] = field(default_factory=list)
    request_id: Optional[str] = None
    raw_response: Optional[Any] = None


@dataclass
class LocalizationResult:
    translated_text: str
    source_locale: str
    target_locale: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    request_id: Optional[str] = None
    raw_response: Optional[Any] = None


@dataclass
class EmbeddingResult:
    embedding: List[float]
    model: str
    input_text: str
    embedding_dimensions: int = 0
    prompt_tokens: int = 0
    request_id: Optional[str] = None
    raw_response: Optional[Any] = None


@dataclass
class AudioBriefResult:
    audio_url: Optional[str] = None
    audio_data: Optional[bytes] = None
    model: str
    input_text: str
    duration_seconds: Optional[float] = None
    format: str = "mp3"
    request_id: Optional[str] = None
    raw_response: Optional[Any] = None


@dataclass
class PlatformResource:
    resource_id: str
    model_name: str
    provider: str
    status: str
    capabilities: List[str] = field(default_factory=list)
    max_tokens: Optional[int] = None
    context_window: Optional[int] = None
    pricing_tier: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_messages(messages: List[Dict[str, str]]) -> List[Message]:
    normalized = []
    for msg in messages:
        role_str = msg.get("role", "user")
        try:
            role = ModelRole(role_str)
        except ValueError:
            role = ModelRole.USER
        normalized.append(Message(role=role, content=msg.get("content", "")))
    return normalized


def build_request_dict(request: PlatformModelRequest) -> Dict[str, Any]:
    result = {
        "model": request.model,
        "messages": [
            {"role": m.role.value, "content": m.content} for m in request.messages
        ],
        "temperature": request.temperature,
        "top_p": request.top_p,
        "stream": request.stream,
    }
    if request.max_tokens is not None:
        result["max_tokens"] = request.max_tokens
    if request.stop is not None:
        result["stop"] = request.stop
    if request.seed is not None:
        result["seed"] = request.seed
    return result
