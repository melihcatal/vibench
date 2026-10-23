import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


DEFAULT_MODEL_FAMILY = "openai"
DEFAULT_MODEL_ID = "openai/gpt-5.4-mini"


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_model_family(model_family: Optional[str]) -> str:
    normalized = normalize_text(model_family).lower()
    if not normalized:
        return DEFAULT_MODEL_FAMILY
    if normalized.startswith("openai"):
        return "openai"
    return normalized


def normalize_model_id(model_id: Optional[str], model_family: Optional[str] = None) -> str:
    normalized = normalize_text(model_id)
    if normalized:
        return normalized
    family = normalize_model_family(model_family)
    if family == "openai":
        return DEFAULT_MODEL_ID
    return DEFAULT_MODEL_ID


def select_model_family(model_id: Optional[str]) -> str:
    normalized = normalize_text(model_id).lower()
    if normalized.startswith("openai/") or normalized.startswith("gpt-") or normalized.startswith("o1"):
        return "openai"
    return DEFAULT_MODEL_FAMILY


@dataclass(frozen=True)
class HostedLLMRequest:
    prompt: str
    context: Optional[str] = None
    model_family: str = DEFAULT_MODEL_FAMILY
    model_id: str = DEFAULT_MODEL_ID
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None
    top_p: Optional[float] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def normalized(self) -> "HostedLLMRequest":
        family = normalize_model_family(self.model_family or select_model_family(self.model_id))
        return HostedLLMRequest(
            prompt=normalize_text(self.prompt),
            context=normalize_text(self.context) or None,
            model_family=family,
            model_id=normalize_model_id(self.model_id, family),
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
            top_p=self.top_p,
            metadata=dict(self.metadata),
        )

    def to_messages(self) -> List[Dict[str, str]]:
        items: List[Dict[str, str]] = []
        if self.context:
            items.append({"role": "system", "content": normalize_text(self.context)})
        items.append({"role": "user", "content": normalize_text(self.prompt)})
        return items

    def to_api_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model_id,
            "messages": self.to_messages(),
        }
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.max_output_tokens is not None:
            payload["max_output_tokens"] = self.max_output_tokens
        if self.top_p is not None:
            payload["top_p"] = self.top_p
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class HostedLLMResponse:
    text: str
    model_family: str = DEFAULT_MODEL_FAMILY
    model_id: str = DEFAULT_MODEL_ID
    raw: Any = None
    usage: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_openai_response(cls, response: Any) -> "HostedLLMResponse":
        text = ""
        output = getattr(response, "output", None)
        if output:
            chunks: List[str] = []
            for item in output:
                content = getattr(item, "content", None)
                if not content:
                    continue
                for part in content:
                    delta = getattr(part, "text", None)
                    if delta:
                        chunks.append(str(delta))
            text = "".join(chunks).strip()
        if not text:
            candidate = getattr(response, "output_text", None)
            if candidate:
                text = normalize_text(candidate)
        model_id = normalize_text(getattr(response, "model", None)) or DEFAULT_MODEL_ID
        model_family = select_model_family(model_id)
        usage = getattr(response, "usage", None) or {}
        return cls(text=text, model_family=model_family, model_id=model_id, raw=response, usage=usage)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "model_family": self.model_family,
            "model_id": self.model_id,
            "usage": dict(self.usage),
        }


def coerce_text_output(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, Mapping):
        if "text" in value:
            return normalize_text(value.get("text"))
        if "content" in value:
            return normalize_text(value.get("content"))
    return normalize_text(value)


def parse_json_output(value: Any) -> Dict[str, Any]:
    text = coerce_text_output(value)
    if not text:
        return {}
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {"text": text}
    if isinstance(parsed, dict):
        return parsed
    return {"value": parsed}


def normalize_request_mapping(request: Mapping[str, Any]) -> HostedLLMRequest:
    data = dict(request)
    return HostedLLMRequest(
        prompt=normalize_text(data.pop("prompt", "")),
        context=normalize_text(data.pop("context", None)) or None,
        model_family=normalize_model_family(data.pop("model_family", None)),
        model_id=normalize_model_id(data.pop("model_id", None), data.get("model_family")),
        temperature=data.pop("temperature", None),
        max_output_tokens=data.pop("max_output_tokens", None),
        top_p=data.pop("top_p", None),
        metadata=data,
    ).normalized()


def normalize_response_mapping(response: Mapping[str, Any]) -> HostedLLMResponse:
    data = dict(response)
    text = coerce_text_output(data.pop("text", data.pop("output_text", "")))
    model_id = normalize_model_id(data.pop("model_id", None), data.get("model_family"))
    model_family = normalize_model_family(data.pop("model_family", None) or select_model_family(model_id))
    usage = data.pop("usage", {})
    return HostedLLMResponse(text=text, model_family=model_family, model_id=model_id, raw=response, usage=usage)
