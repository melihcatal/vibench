from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Union


@dataclass
class ModelFamilySelectionRequest:
    provider: str
    family: str
    preferred_model_id: Optional[str] = None
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HostedLLMInferenceRequest:
    model: str
    messages: List[Dict[str, Any]]
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None
    top_p: Optional[float] = None
    stream: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HostedLLMInferenceResponse:
    model: str
    output_text: str
    raw: Dict[str, Any] = field(default_factory=dict)
    usage: Dict[str, Any] = field(default_factory=dict)
    normalized: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelFamilySelectionResponse:
    provider: str
    family: str
    selected_model_id: str
    rationale: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_model_family_selection(data: Union[Dict[str, Any], ModelFamilySelectionRequest]) -> ModelFamilySelectionRequest:
    if isinstance(data, ModelFamilySelectionRequest):
        return data
    return ModelFamilySelectionRequest(
        provider=str(data.get("provider", "")),
        family=str(data.get("family", "")),
        preferred_model_id=data.get("preferred_model_id"),
        temperature=data.get("temperature"),
        max_output_tokens=data.get("max_output_tokens"),
        metadata=dict(data.get("metadata") or {}),
    )


def normalize_hosted_llm_inference_request(data: Union[Dict[str, Any], HostedLLMInferenceRequest]) -> HostedLLMInferenceRequest:
    if isinstance(data, HostedLLMInferenceRequest):
        return data
    messages = data.get("messages") or []
    if not isinstance(messages, list):
        raise TypeError("messages must be a list")
    return HostedLLMInferenceRequest(
        model=str(data.get("model", "")),
        messages=[dict(message) for message in messages],
        temperature=data.get("temperature"),
        max_output_tokens=data.get("max_output_tokens"),
        top_p=data.get("top_p"),
        stream=bool(data.get("stream", False)),
        metadata=dict(data.get("metadata") or {}),
    )


def normalize_hosted_llm_inference_response(data: Union[Dict[str, Any], HostedLLMInferenceResponse]) -> HostedLLMInferenceResponse:
    if isinstance(data, HostedLLMInferenceResponse):
        return data
    raw = dict(data)
    model = str(raw.get("model", ""))
    output_text = _extract_output_text(raw)
    return HostedLLMInferenceResponse(
        model=model,
        output_text=output_text,
        raw=raw,
        usage=dict(raw.get("usage") or {}),
        normalized={
            "provider": raw.get("provider"),
            "model": model,
            "output_text": output_text,
        },
    )


def normalize_model_family_selection_response(data: Union[Dict[str, Any], ModelFamilySelectionResponse]) -> ModelFamilySelectionResponse:
    if isinstance(data, ModelFamilySelectionResponse):
        return data
    raw = dict(data)
    return ModelFamilySelectionResponse(
        provider=str(raw.get("provider", "")),
        family=str(raw.get("family", "")),
        selected_model_id=str(raw.get("selected_model_id", raw.get("model", ""))),
        rationale=raw.get("rationale"),
        raw=raw,
    )


def _extract_output_text(raw: Dict[str, Any]) -> str:
    if isinstance(raw.get("output_text"), str):
        return raw["output_text"]
    if isinstance(raw.get("text"), str):
        return raw["text"]
    choices = raw.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0] or {}
        if isinstance(first, dict):
            message = first.get("message") or {}
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
            if isinstance(first.get("text"), str):
                return first["text"]
    content = raw.get("content")
    if isinstance(content, str):
        return content
    return ""
