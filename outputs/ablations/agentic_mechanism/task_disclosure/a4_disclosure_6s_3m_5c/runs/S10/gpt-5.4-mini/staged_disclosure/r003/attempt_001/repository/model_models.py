from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Sequence


def _strip_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _normalize_alias(value: Optional[str]) -> Optional[str]:
    value = _strip_string(value)
    if value is None:
        return None
    return value.lower().replace("_", "-")


@dataclass(frozen=True)
class HostedLLMInferenceRequest:
    provider: str
    model: str
    prompt: str
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    extra: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "provider", _normalize_alias(self.provider) or "")
        object.__setattr__(self, "model", _strip_string(self.model) or "")
        object.__setattr__(self, "prompt", _strip_string(self.prompt) or "")


@dataclass(frozen=True)
class HostedLLMInferenceResponse:
    provider: str
    model: str
    output_text: str
    raw: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "provider", _normalize_alias(self.provider) or "")
        object.__setattr__(self, "model", _strip_string(self.model) or "")
        object.__setattr__(self, "output_text", _strip_string(self.output_text) or "")


@dataclass(frozen=True)
class ModelFamilySelection:
    family: str
    preferred_provider: Optional[str] = None
    preferred_model: Optional[str] = None
    fallback_models: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "family", _normalize_alias(self.family) or "")
        object.__setattr__(self, "preferred_provider", _normalize_alias(self.preferred_provider))
        object.__setattr__(self, "preferred_model", _strip_string(self.preferred_model))
        object.__setattr__(self, "fallback_models", tuple(m for m in (_strip_string(x) for x in self.fallback_models) if m))


def normalize_provider_name(value: Optional[str]) -> Optional[str]:
    return _normalize_alias(value)


def normalize_model_name(value: Optional[str]) -> Optional[str]:
    return _strip_string(value)


def normalize_model_family(value: Optional[str]) -> Optional[str]:
    value = _normalize_alias(value)
    if value is None:
        return None
    if value.endswith("-family"):
        return value
    return f"{value}-family"


def normalize_inference_request(data: Mapping[str, Any]) -> HostedLLMInferenceRequest:
    provider = _normalize_alias(data.get("provider")) or ""
    model = _strip_string(data.get("model")) or ""
    prompt = _strip_string(data.get("prompt")) or ""
    temperature = data.get("temperature")
    max_tokens = data.get("max_tokens")
    extra = {k: v for k, v in data.items() if k not in {"provider", "model", "prompt", "temperature", "max_tokens"}}
    return HostedLLMInferenceRequest(
        provider=provider,
        model=model,
        prompt=prompt,
        temperature=float(temperature) if temperature is not None else None,
        max_tokens=int(max_tokens) if max_tokens is not None else None,
        extra=extra,
    )


def normalize_inference_response(data: Mapping[str, Any]) -> HostedLLMInferenceResponse:
    provider = _normalize_alias(data.get("provider")) or ""
    model = _strip_string(data.get("model")) or ""
    output_text = _strip_string(data.get("output_text") or data.get("text") or data.get("content")) or ""
    raw = dict(data)
    return HostedLLMInferenceResponse(provider=provider, model=model, output_text=output_text, raw=raw)


def select_model_family(preferred: Optional[str], candidates: Sequence[str]) -> ModelFamilySelection:
    family = normalize_model_family(preferred) or ""
    normalized_candidates = tuple(m for m in (_strip_string(x) for x in candidates) if m)
    preferred_model = normalized_candidates[0] if normalized_candidates else None
    return ModelFamilySelection(family=family, preferred_model=preferred_model, fallback_models=normalized_candidates[1:])
