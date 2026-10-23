from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence


@dataclass(frozen=True)
class PlatformMessage:
    role: str
    content: str
    name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"role": self.role, "content": self.content}
        if self.name is not None:
            data["name"] = self.name
        return data


@dataclass(frozen=True)
class PlatformRequest:
    model: str
    messages: Sequence[PlatformMessage] = field(default_factory=tuple)
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [message.to_dict() for message in self.messages],
        }
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.top_p is not None:
            payload["top_p"] = self.top_p
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class PlatformUsage:
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["PlatformUsage"]:
        if not data:
            return None
        return cls(
            input_tokens=data.get("input_tokens") or data.get("prompt_tokens"),
            output_tokens=data.get("output_tokens") or data.get("completion_tokens"),
            total_tokens=data.get("total_tokens"),
        )


@dataclass(frozen=True)
class PlatformResponse:
    text: str
    model: Optional[str] = None
    resource_id: Optional[str] = None
    model_handle: Optional[str] = None
    usage: Optional[PlatformUsage] = None
    raw: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlatformResponse":
        text = _extract_text(data)
        return cls(
            text=text,
            model=data.get("model"),
            resource_id=data.get("resource_id") or data.get("id"),
            model_handle=data.get("model_handle") or data.get("deployment_id") or data.get("inference_profile_id"),
            usage=PlatformUsage.from_dict(data.get("usage")),
            raw=data,
        )


def normalize_messages(messages: Sequence[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for message in messages:
        if isinstance(message, PlatformMessage):
            normalized.append(message.to_dict())
        elif isinstance(message, dict):
            role = str(message.get("role", "user"))
            content = str(message.get("content", ""))
            item: Dict[str, Any] = {"role": role, "content": content}
            if message.get("name") is not None:
                item["name"] = message["name"]
            normalized.append(item)
        else:
            normalized.append({"role": "user", "content": str(message)})
    return normalized


def normalize_request(request: Any) -> Dict[str, Any]:
    if isinstance(request, PlatformRequest):
        return request.to_dict()
    if isinstance(request, dict):
        payload = dict(request)
        if "messages" in payload:
            payload["messages"] = normalize_messages(payload["messages"])
        return payload
    raise TypeError("request must be a PlatformRequest or dict")


def normalize_response(response: Any) -> PlatformResponse:
    if isinstance(response, PlatformResponse):
        return response
    if isinstance(response, dict):
        return PlatformResponse.from_dict(response)
    if hasattr(response, "to_dict"):
        data = response.to_dict()
        if isinstance(data, dict):
            return PlatformResponse.from_dict(data)
    raise TypeError("response must be a PlatformResponse or mapping-like object")


def _extract_text(data: Dict[str, Any]) -> str:
    if isinstance(data.get("text"), str):
        return data["text"]
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
            if isinstance(first.get("text"), str):
                return first["text"]
    return ""
