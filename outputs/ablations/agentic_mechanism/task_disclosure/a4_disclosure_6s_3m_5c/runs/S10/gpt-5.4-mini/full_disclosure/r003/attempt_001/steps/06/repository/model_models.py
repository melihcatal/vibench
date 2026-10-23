import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


DEFAULT_MODEL_FAMILY = os.getenv("OPENAI_MODEL_FAMILY", "gpt-5")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


@dataclass(frozen=True)
class ModelSelection:
    family: str = DEFAULT_MODEL_FAMILY
    model: str = DEFAULT_MODEL


@dataclass(frozen=True)
class Message:
    role: str
    content: Union[str, Sequence[Mapping[str, Any]]]


@dataclass(frozen=True)
class CompletionRequest:
    messages: Sequence[Message]
    model: str = DEFAULT_MODEL
    family: str = DEFAULT_MODEL_FAMILY
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [normalize_message(message) for message in self.messages],
            "metadata": dict(self.metadata),
        }
        if self.max_output_tokens is not None:
            payload["max_output_tokens"] = self.max_output_tokens
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.top_p is not None:
            payload["top_p"] = self.top_p
        return payload


@dataclass(frozen=True)
class CompletionChoice:
    index: int
    text: str
    message: Optional[Dict[str, Any]] = None
    finish_reason: Optional[str] = None


@dataclass(frozen=True)
class CompletionResponse:
    model: str
    family: str
    output_text: str
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_message(message: Union[Message, Mapping[str, Any]]) -> Dict[str, Any]:
    if isinstance(message, Message):
        return {"role": message.role, "content": message.content}
    return {"role": message["role"], "content": message["content"]}


def normalize_selection(model: Optional[str] = None, family: Optional[str] = None) -> ModelSelection:
    return ModelSelection(
        family=family or DEFAULT_MODEL_FAMILY,
        model=model or DEFAULT_MODEL,
    )


def normalize_completion_request(
    messages: Sequence[Union[Message, Mapping[str, Any]]],
    model: Optional[str] = None,
    family: Optional[str] = None,
    max_output_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    metadata: Optional[Mapping[str, Any]] = None,
) -> CompletionRequest:
    selection = normalize_selection(model=model, family=family)
    return CompletionRequest(
        messages=[m if isinstance(m, Message) else Message(role=m["role"], content=m["content"]) for m in messages],
        model=selection.model,
        family=selection.family,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        metadata=dict(metadata or {}),
    )


def normalize_completion_choice(choice: Mapping[str, Any]) -> CompletionChoice:
    message = choice.get("message")
    text = choice.get("text")
    if text is None and isinstance(message, Mapping):
        content = message.get("content")
        text = content if isinstance(content, str) else ""
    return CompletionChoice(
        index=int(choice.get("index", 0)),
        text=text or "",
        message=dict(message) if isinstance(message, Mapping) else None,
        finish_reason=choice.get("finish_reason"),
    )


def normalize_completion_response(payload: Mapping[str, Any]) -> CompletionResponse:
    model = str(payload.get("model", DEFAULT_MODEL))
    family = str(payload.get("family", DEFAULT_MODEL_FAMILY))
    output_text = payload.get("output_text")
    if output_text is None:
        choices = payload.get("choices") or []
        if choices:
            choice = normalize_completion_choice(choices[0])
            output_text = choice.text
        else:
            output_text = ""
    return CompletionResponse(model=model, family=family, output_text=str(output_text), raw=dict(payload))


def coerce_model_family(model: Optional[str] = None, family: Optional[str] = None) -> str:
    return normalize_selection(model=model, family=family).family


def coerce_model_name(model: Optional[str] = None, family: Optional[str] = None) -> str:
    return normalize_selection(model=model, family=family).model
