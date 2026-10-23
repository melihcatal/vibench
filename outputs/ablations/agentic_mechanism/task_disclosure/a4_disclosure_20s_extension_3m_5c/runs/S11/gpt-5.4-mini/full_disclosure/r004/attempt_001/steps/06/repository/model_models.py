from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union


@dataclass(frozen=True)
class PlatformMessage:
    role: str
    content: str


@dataclass(frozen=True)
class PlatformRequest:
    model: str
    messages: Tuple[PlatformMessage, ...] = field(default_factory=tuple)
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    stop: Optional[Tuple[str, ...]] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlatformUsage:
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


@dataclass(frozen=True)
class PlatformChoice:
    index: int
    message: PlatformMessage
    finish_reason: Optional[str] = None


@dataclass(frozen=True)
class PlatformResponse:
    output_text: str
    model: Optional[str] = None
    provider: Optional[str] = None
    resource_id: Optional[str] = None
    usage: Optional[PlatformUsage] = None
    raw: Any = None
    choices: Tuple[PlatformChoice, ...] = field(default_factory=tuple)


def normalize_messages(messages: Iterable[Union[PlatformMessage, Mapping[str, Any], Sequence[Any]]]) -> Tuple[PlatformMessage, ...]:
    normalized: List[PlatformMessage] = []
    for message in messages:
        if isinstance(message, PlatformMessage):
            normalized.append(message)
            continue
        if isinstance(message, Mapping):
            role = str(message.get("role", "user"))
            content = str(message.get("content", ""))
            normalized.append(PlatformMessage(role=role, content=content))
            continue
        if isinstance(message, Sequence) and len(message) >= 2 and not isinstance(message, (str, bytes, bytearray)):
            normalized.append(PlatformMessage(role=str(message[0]), content=str(message[1])))
            continue
        raise TypeError(f"Unsupported message format: {type(message)!r}")
    return tuple(normalized)


def normalize_request(request: Union[PlatformRequest, Mapping[str, Any]]) -> PlatformRequest:
    if isinstance(request, PlatformRequest):
        return request
    if not isinstance(request, Mapping):
        raise TypeError(f"Unsupported request format: {type(request)!r}")
    messages = normalize_messages(request.get("messages", ()))
    stop = request.get("stop")
    stop_tuple = None
    if stop is not None:
        if isinstance(stop, (str, bytes, bytearray)):
            stop_tuple = (str(stop),)
        else:
            stop_tuple = tuple(str(item) for item in stop)
    return PlatformRequest(
        model=str(request["model"]),
        messages=messages,
        temperature=request.get("temperature"),
        max_tokens=request.get("max_tokens"),
        top_p=request.get("top_p"),
        stop=stop_tuple,
        metadata=dict(request.get("metadata", {})),
    )


def normalize_usage(usage: Optional[Union[PlatformUsage, Mapping[str, Any]]]) -> Optional[PlatformUsage]:
    if usage is None or isinstance(usage, PlatformUsage):
        return usage
    if not isinstance(usage, Mapping):
        raise TypeError(f"Unsupported usage format: {type(usage)!r}")
    return PlatformUsage(
        prompt_tokens=usage.get("prompt_tokens"),
        completion_tokens=usage.get("completion_tokens"),
        total_tokens=usage.get("total_tokens"),
    )


def _extract_content_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, Mapping):
        if "text" in content:
            return str(content["text"])
        if "content" in content:
            return _extract_content_text(content["content"])
    if isinstance(content, Sequence) and not isinstance(content, (str, bytes, bytearray)):
        parts = [_extract_content_text(item) for item in content]
        return "".join(part for part in parts if part)
    return str(content)


def normalize_response(response: Any) -> PlatformResponse:
    if isinstance(response, PlatformResponse):
        return response

    model = None
    provider = None
    resource_id = None
    usage = None
    raw = response
    choices: Tuple[PlatformChoice, ...] = tuple()
    output_text = ""

    if isinstance(response, Mapping):
        model = response.get("model") or response.get("model_id") or response.get("model_name")
        provider = response.get("provider")
        resource_id = response.get("resource_id") or response.get("id") or response.get("deployment_id") or response.get("inference_profile_id")
        usage = normalize_usage(response.get("usage"))
        if "choices" in response and isinstance(response["choices"], Sequence):
            parsed_choices: List[PlatformChoice] = []
            for idx, choice in enumerate(response["choices"]):
                if not isinstance(choice, Mapping):
                    continue
                message_data = choice.get("message") or choice.get("delta") or {}
                if isinstance(message_data, Mapping):
                    role = str(message_data.get("role", "assistant"))
                    content = _extract_content_text(message_data.get("content"))
                else:
                    role = "assistant"
                    content = _extract_content_text(message_data)
                parsed_choices.append(
                    PlatformChoice(
                        index=int(choice.get("index", idx)),
                        message=PlatformMessage(role=role, content=content),
                        finish_reason=choice.get("finish_reason"),
                    )
                )
            choices = tuple(parsed_choices)
            if choices:
                output_text = choices[0].message.content
        if not output_text:
            for key in ("output_text", "text", "content"):
                if key in response:
                    output_text = _extract_content_text(response.get(key))
                    break
        if not output_text and "output" in response:
            output_text = _extract_content_text(response.get("output"))
        if not output_text and "message" in response:
            output_text = _extract_content_text(response.get("message"))
    else:
        output_text = _extract_content_text(response)

    return PlatformResponse(
        output_text=output_text,
        model=str(model) if model is not None else None,
        provider=str(provider) if provider is not None else None,
        resource_id=str(resource_id) if resource_id is not None else None,
        usage=usage,
        raw=raw,
        choices=choices,
    )
