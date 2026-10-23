import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


DEFAULT_MODEL_FAMILY = "gpt-5"
DEFAULT_MODEL_ID = "openai/gpt-5.4-mini"


@dataclass(frozen=True)
class ModelSelection:
    family: str = DEFAULT_MODEL_FAMILY
    model_id: str = DEFAULT_MODEL_ID


@dataclass(frozen=True)
class HostedLLMRequest:
    input: Any
    model_family: str = DEFAULT_MODEL_FAMILY
    model_id: Optional[str] = None
    temperature: float = 0.2
    max_output_tokens: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HostedLLMResponse:
    model_family: str
    model_id: str
    output_text: str = ""
    raw: Any = None


def get_default_model_family() -> str:
    return os.getenv("MODEL_FAMILY", DEFAULT_MODEL_FAMILY)


def get_default_model_id() -> str:
    return os.getenv("MODEL_ID", DEFAULT_MODEL_ID)


def normalize_model_family(model_family: Optional[str]) -> str:
    family = (model_family or get_default_model_family()).strip().lower()
    if family in {"gpt5", "gpt-5", "gpt 5"}:
        return "gpt-5"
    if family in {"gpt4.1", "gpt-4.1", "gpt4", "gpt-4"}:
        return "gpt-4.1"
    return family


def normalize_model_id(model_family: Optional[str] = None, model_id: Optional[str] = None) -> str:
    if model_id:
        return model_id
    family = normalize_model_family(model_family)
    if family == "gpt-5":
        return get_default_model_id()
    if family == "gpt-4.1":
        return os.getenv("MODEL_ID", "openai/gpt-4.1")
    return get_default_model_id()


def select_model(model_family: Optional[str] = None, model_id: Optional[str] = None) -> ModelSelection:
    family = normalize_model_family(model_family)
    resolved_model_id = normalize_model_id(family, model_id)
    return ModelSelection(family=family, model_id=resolved_model_id)


def build_request(
    input: Any,
    *,
    model_family: Optional[str] = None,
    model_id: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: Optional[int] = None,
    **extra: Any,
) -> HostedLLMRequest:
    selection = select_model(model_family=model_family, model_id=model_id)
    return HostedLLMRequest(
        input=input,
        model_family=selection.family,
        model_id=selection.model_id,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        extra=dict(extra),
    )


def request_to_payload(request: HostedLLMRequest) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": request.model_id or normalize_model_id(request.model_family, None),
        "input": request.input,
        "temperature": request.temperature,
        **request.extra,
    }
    if request.max_output_tokens is not None:
        payload["max_output_tokens"] = request.max_output_tokens
    return payload


def response_from_api(data: Any, *, model_family: Optional[str] = None, model_id: Optional[str] = None) -> HostedLLMResponse:
    resolved = select_model(model_family=model_family, model_id=model_id)
    output_text = getattr(data, "output_text", None)
    if output_text is None and isinstance(data, Mapping):
        output_text = data.get("output_text", "")
    if output_text is None:
        output_text = ""
    return HostedLLMResponse(model_family=resolved.family, model_id=resolved.model_id, output_text=output_text, raw=data)


def normalize_messages(messages: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for message in messages:
        role = str(message.get("role", "user")).strip().lower()
        content = message.get("content", "")
        normalized.append({"role": role, "content": content})
    return normalized
