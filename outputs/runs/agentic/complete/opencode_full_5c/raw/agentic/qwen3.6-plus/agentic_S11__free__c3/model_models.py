from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformRequest:
    model_id: str
    messages: List[Dict[str, str]]
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    stop: Optional[List[str]] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformResponse:
    content: str
    model_id: str
    finish_reason: Optional[str] = None
    request_id: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    raw_response: Optional[Any] = None


@dataclass
class StreamChunk:
    content: str
    index: int
    finish_reason: Optional[str] = None
    raw_chunk: Optional[Any] = None


@dataclass
class PlatformMetadata:
    model_id: str
    request_id: Optional[str] = None
    organization_id: Optional[str] = None
    usage_prompt_tokens: int = 0
    usage_completion_tokens: int = 0
    usage_total_tokens: int = 0
    system_fingerprint: Optional[str] = None
    created: Optional[int] = None
    raw_response: Optional[Any] = None


@dataclass
class SafetyResult:
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    raw_response: Optional[Any] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_locale: str
    target_locale: str
    model_id: str
    usage: Optional[Dict[str, int]] = None
    raw_response: Optional[Any] = None


@dataclass
class EmbeddingResult:
    embedding: List[float]
    model_id: str
    usage_prompt_tokens: int = 0
    raw_response: Optional[Any] = None


@dataclass
class AudioResult:
    audio_data: bytes
    model_id: str
    format: str = "mp3"
    usage: Optional[Dict[str, int]] = None
    raw_response: Optional[Any] = None


def normalize_messages(
    prompt: str,
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": prompt})
    return messages


def build_platform_request(
    prompt: str,
    model_id: str,
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    stream: bool = False,
    stop: Optional[List[str]] = None,
    extra_params: Optional[Dict[str, Any]] = None,
) -> PlatformRequest:
    messages = normalize_messages(prompt, system_prompt, conversation_history)
    return PlatformRequest(
        model_id=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=stream,
        stop=stop,
        extra_params=extra_params or {},
    )


def extract_usage_from_openai_response(response: Any) -> Dict[str, int]:
    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    if hasattr(response, "usage") and response.usage:
        usage["prompt_tokens"] = getattr(response.usage, "prompt_tokens", 0)
        usage["completion_tokens"] = getattr(response.usage, "completion_tokens", 0)
        usage["total_tokens"] = getattr(response.usage, "total_tokens", 0)
    return usage


def extract_metadata_from_openai_response(response: Any) -> PlatformMetadata:
    usage = extract_usage_from_openai_response(response)
    return PlatformMetadata(
        model_id=getattr(response, "model", ""),
        request_id=getattr(response, "id", None),
        organization_id=getattr(response, "organization", None),
        usage_prompt_tokens=usage["prompt_tokens"],
        usage_completion_tokens=usage["completion_tokens"],
        usage_total_tokens=usage["total_tokens"],
        system_fingerprint=getattr(response, "system_fingerprint", None),
        created=getattr(response, "created", None),
        raw_response=response,
    )
