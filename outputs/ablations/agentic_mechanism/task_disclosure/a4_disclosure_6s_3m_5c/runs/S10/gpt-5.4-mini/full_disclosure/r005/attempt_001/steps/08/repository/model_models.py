from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Union


MessageContent = Union[str, Sequence[Dict[str, Any]]]


@dataclass(frozen=True)
class RequestMessage:
    role: str
    content: MessageContent


@dataclass(frozen=True)
class HostedLLMRequest:
    model: str
    messages: List[RequestMessage]
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None
    top_p: Optional[float] = None
    response_format: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HostedLLMChoice:
    index: int
    role: str
    content: str
    finish_reason: Optional[str] = None


@dataclass(frozen=True)
class HostedLLMResponse:
    model: str
    output_text: str
    choices: List[HostedLLMChoice]
    usage: Optional[Dict[str, int]] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class ModelFamilySelection:
    model: str
    family: str
    provider: str = "openai"


def normalize_model_name(model: Optional[str]) -> str:
    if not model:
        return "openai/gpt-5.4-mini"
    return model


def normalize_model_family(model: Optional[str]) -> str:
    normalized = normalize_model_name(model)
    if "/" in normalized:
        normalized = normalized.split("/", 1)[1]
    if normalized.startswith("gpt-"):
        parts = normalized.split("-")
        if len(parts) >= 2:
            return "-".join(parts[:2])
    return "gpt-5.4"


def make_selection(model: Optional[str] = None) -> ModelFamilySelection:
    selected_model = normalize_model_name(model)
    return ModelFamilySelection(model=selected_model, family=normalize_model_family(selected_model))


def normalize_request_messages(messages: Sequence[Dict[str, Any]]) -> List[RequestMessage]:
    normalized: List[RequestMessage] = []
    for message in messages:
        normalized.append(RequestMessage(role=str(message.get("role", "user")), content=message.get("content", "")))
    return normalized


def normalize_response(payload: Dict[str, Any]) -> HostedLLMResponse:
    model = str(payload.get("model", ""))
    choices_payload = payload.get("choices") or []
    choices: List[HostedLLMChoice] = []
    for choice in choices_payload:
        message = choice.get("message") or {}
        choices.append(
            HostedLLMChoice(
                index=int(choice.get("index", len(choices))),
                role=str(message.get("role", "assistant")),
                content=str(message.get("content", "")),
                finish_reason=choice.get("finish_reason"),
            )
        )
    output_text = choices[0].content if choices else str(payload.get("output_text", ""))
    usage = payload.get("usage")
    return HostedLLMResponse(model=model, output_text=output_text, choices=choices, usage=usage, raw=payload)
