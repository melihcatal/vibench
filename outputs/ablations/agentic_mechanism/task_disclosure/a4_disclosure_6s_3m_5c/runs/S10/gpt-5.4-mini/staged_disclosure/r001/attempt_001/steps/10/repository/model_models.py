from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


@dataclass(frozen=True)
class HostedLLMInferenceRequest:
    provider: str
    model: str
    prompt: Optional[str] = None
    messages: Optional[Sequence[Mapping[str, Any]]] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    stop: Optional[Union[str, Sequence[str]]] = None
    metadata: Optional[Mapping[str, Any]] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"model": self.model}
        if self.prompt is not None:
            payload["prompt"] = self.prompt
        if self.messages is not None:
            payload["messages"] = [dict(message) for message in self.messages]
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        if self.top_p is not None:
            payload["top_p"] = self.top_p
        if self.stop is not None:
            payload["stop"] = self.stop
        if self.metadata is not None:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class HostedLLMInferenceResponse:
    provider: str
    model: str
    text: str
    raw: Mapping[str, Any]
    finish_reason: Optional[str] = None
    usage: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class ModelFamilySelectionRequest:
    provider: str
    family: str
    task: Optional[str] = None
    latency_priority: Optional[str] = None
    quality_priority: Optional[str] = None
    budget_priority: Optional[str] = None
    region: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"family": self.family}
        if self.task is not None:
            payload["task"] = self.task
        if self.latency_priority is not None:
            payload["latency_priority"] = self.latency_priority
        if self.quality_priority is not None:
            payload["quality_priority"] = self.quality_priority
        if self.budget_priority is not None:
            payload["budget_priority"] = self.budget_priority
        if self.region is not None:
            payload["region"] = self.region
        return payload


@dataclass(frozen=True)
class ModelFamilySelectionResponse:
    provider: str
    family: str
    selected_model: str
    rationale: Optional[str]
    raw: Mapping[str, Any]


def normalize_hosted_llm_inference_response(provider: str, raw: Mapping[str, Any]) -> HostedLLMInferenceResponse:
    model = str(raw.get("model", ""))
    text = _extract_text(raw)
    finish_reason = _extract_finish_reason(raw)
    usage = raw.get("usage") if isinstance(raw.get("usage"), Mapping) else None
    return HostedLLMInferenceResponse(
        provider=provider,
        model=model,
        text=text,
        raw=raw,
        finish_reason=finish_reason,
        usage=usage,
    )


def normalize_model_family_selection_response(provider: str, family: str, raw: Mapping[str, Any]) -> ModelFamilySelectionResponse:
    selected_model = str(
        raw.get("selected_model")
        or raw.get("model")
        or raw.get("name")
        or raw.get("id")
        or ""
    )
    rationale = raw.get("rationale")
    if rationale is not None:
        rationale = str(rationale)
    return ModelFamilySelectionResponse(
        provider=provider,
        family=family,
        selected_model=selected_model,
        rationale=rationale,
        raw=raw,
    )


def _extract_text(raw: Mapping[str, Any]) -> str:
    if isinstance(raw.get("text"), str):
        return raw["text"]
    choices = raw.get("choices")
    if isinstance(choices, Sequence):
        for choice in choices:
            if not isinstance(choice, Mapping):
                continue
            message = choice.get("message")
            if isinstance(message, Mapping) and isinstance(message.get("content"), str):
                return message["content"]
            if isinstance(choice.get("text"), str):
                return choice["text"]
    if isinstance(raw.get("output_text"), str):
        return raw["output_text"]
    return ""


def _extract_finish_reason(raw: Mapping[str, Any]) -> Optional[str]:
    choices = raw.get("choices")
    if isinstance(choices, Sequence) and choices:
        first = choices[0]
        if isinstance(first, Mapping):
            reason = first.get("finish_reason")
            if reason is not None:
                return str(reason)
    if raw.get("finish_reason") is not None:
        return str(raw.get("finish_reason"))
    return None
