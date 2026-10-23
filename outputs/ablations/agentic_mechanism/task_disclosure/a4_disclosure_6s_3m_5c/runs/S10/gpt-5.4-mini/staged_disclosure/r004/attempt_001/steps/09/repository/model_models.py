import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple


DEFAULT_MODEL_FAMILY = os.getenv("MODEL_FAMILY", "gpt-5")
DEFAULT_MODEL_ID = os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini")


def _clean_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _clean_optional_str(value: Any) -> Optional[str]:
    text = _clean_str(value)
    return text or None


def _clean_messages(messages: Any) -> List[Dict[str, str]]:
    if messages is None:
        return []
    normalized: List[Dict[str, str]] = []
    for item in messages:
        if isinstance(item, dict):
            role = _clean_str(item.get("role")) or "user"
            content = _clean_str(item.get("content"))
        elif isinstance(item, (tuple, list)) and len(item) >= 2:
            role = _clean_str(item[0]) or "user"
            content = _clean_str(item[1])
        else:
            role = "user"
            content = _clean_str(item)
        normalized.append({"role": role, "content": content})
    return normalized


def select_model_family(family: Optional[str] = None) -> str:
    candidate = _clean_str(family or os.getenv("MODEL_FAMILY") or DEFAULT_MODEL_FAMILY).lower()
    if candidate in {"gpt-5", "gpt5", "5"}:
        return "gpt-5"
    if candidate in {"gpt-4.1", "gpt4.1", "4.1"}:
        return "gpt-4.1"
    if candidate in {"gpt-4o", "gpt4o", "4o"}:
        return "gpt-4o"
    return candidate or "gpt-5"


def select_model_id(family: Optional[str] = None, model_id: Optional[str] = None) -> str:
    resolved_family = select_model_family(family)
    if model_id:
        return _clean_str(model_id)
    mapping = {
        "gpt-5": os.getenv("OPENAI_MODEL_GPT5", DEFAULT_MODEL_ID),
        "gpt-4.1": os.getenv("OPENAI_MODEL_GPT41", "openai/gpt-4.1"),
        "gpt-4o": os.getenv("OPENAI_MODEL_GPT4O", "openai/gpt-4o"),
    }
    return mapping.get(resolved_family, os.getenv("OPENAI_MODEL", DEFAULT_MODEL_ID))


@dataclass(frozen=True)
class HostedLLMRequest:
    messages: List[Dict[str, str]] = field(default_factory=list)
    model_family: str = DEFAULT_MODEL_FAMILY
    model_id: str = DEFAULT_MODEL_ID
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    stream: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, value: Any) -> "HostedLLMRequest":
        if isinstance(value, cls):
            return value
        if value is None:
            return cls()
        if isinstance(value, dict):
            family = select_model_family(value.get("model_family") or value.get("family"))
            model_id = select_model_id(family, value.get("model_id") or value.get("model"))
            return cls(
                messages=_clean_messages(value.get("messages")),
                model_family=family,
                model_id=model_id,
                temperature=value.get("temperature"),
                max_tokens=value.get("max_tokens") or value.get("max_output_tokens"),
                top_p=value.get("top_p"),
                stream=bool(value.get("stream", False)),
                metadata=dict(value.get("metadata") or {}),
            )
        messages = getattr(value, "messages", None)
        family = select_model_family(getattr(value, "model_family", None))
        model_id = select_model_id(family, getattr(value, "model_id", None))
        return cls(
            messages=_clean_messages(messages),
            model_family=family,
            model_id=model_id,
            temperature=getattr(value, "temperature", None),
            max_tokens=getattr(value, "max_tokens", None),
            top_p=getattr(value, "top_p", None),
            stream=bool(getattr(value, "stream", False)),
            metadata=dict(getattr(value, "metadata", {}) or {}),
        )


@dataclass(frozen=True)
class HostedLLMResponse:
    model_family: str
    model_id: str
    content: str = ""
    raw: Any = None
    finish_reason: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    normalized: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_provider(cls, value: Any, request: Optional[HostedLLMRequest] = None) -> "HostedLLMResponse":
        request = request or HostedLLMRequest.normalize(None)
        if value is None:
            return cls(model_family=request.model_family, model_id=request.model_id)
        content = ""
        finish_reason = None
        usage: Dict[str, Any] = {}
        normalized: Dict[str, Any] = {}
        if isinstance(value, dict):
            normalized = dict(value)
            usage = dict(value.get("usage") or {})
            finish_reason = _clean_optional_str(value.get("finish_reason"))
            content = _clean_str(value.get("content") or value.get("output_text") or value.get("text"))
        else:
            content = _clean_str(getattr(value, "content", None) or getattr(value, "output_text", None) or getattr(value, "text", None))
            finish_reason = _clean_optional_str(getattr(value, "finish_reason", None))
            usage = dict(getattr(value, "usage", {}) or {})
            normalized = {
                "id": getattr(value, "id", None),
                "model": getattr(value, "model", None),
            }
        return cls(
            model_family=request.model_family,
            model_id=getattr(value, "model", None) or request.model_id,
            content=content,
            raw=value,
            finish_reason=finish_reason,
            usage=usage,
            normalized=normalized,
        )


def normalize_request(value: Any) -> HostedLLMRequest:
    return HostedLLMRequest.normalize(value)


def normalize_response(value: Any, request: Optional[Any] = None) -> HostedLLMResponse:
    return HostedLLMResponse.from_provider(value, HostedLLMRequest.normalize(request))


def build_request(
    messages: Sequence[Any],
    model_family: Optional[str] = None,
    model_id: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
    stream: bool = False,
    metadata: Optional[Dict[str, Any]] = None,
) -> HostedLLMRequest:
    family = select_model_family(model_family)
    resolved_model_id = select_model_id(family, model_id)
    return HostedLLMRequest(
        messages=_clean_messages(messages),
        model_family=family,
        model_id=resolved_model_id,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=stream,
        metadata=dict(metadata or {}),
    )
