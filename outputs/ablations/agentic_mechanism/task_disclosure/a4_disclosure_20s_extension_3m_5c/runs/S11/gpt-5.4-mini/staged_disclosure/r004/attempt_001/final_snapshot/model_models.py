from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


def _coerce_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return str(value)


def _coerce_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "y", "on"}:
            return True
        if normalized in {"false", "0", "no", "n", "off"}:
            return False
    return None


def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            return int(stripped)
        except ValueError:
            return None
    return None


def _coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            return float(stripped)
        except ValueError:
            return None
    return None


def _normalize_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


@dataclass(slots=True)
class ModelRequest:
    model_id: Optional[str] = None
    prompt: Optional[str] = None
    input_data: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    stream: Optional[bool] = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ModelRequest":
        data = dict(payload)
        return cls(
            model_id=_coerce_str(data.get("model_id") or data.get("modelId") or data.get("model")),
            prompt=_coerce_str(data.get("prompt") or data.get("input") or data.get("text")),
            input_data=_normalize_mapping(data.get("input_data") or data.get("inputData") or data.get("data")),
            parameters=_normalize_mapping(data.get("parameters") or data.get("params") or data.get("options")),
            stream=_coerce_bool(data.get("stream")),
        )

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.model_id is not None:
            payload["model_id"] = self.model_id
        if self.prompt is not None:
            payload["prompt"] = self.prompt
        if self.input_data:
            payload["input_data"] = dict(self.input_data)
        if self.parameters:
            payload["parameters"] = dict(self.parameters)
        if self.stream is not None:
            payload["stream"] = self.stream
        return payload


@dataclass(slots=True)
class ModelResponse:
    request_id: Optional[str] = None
    model_id: Optional[str] = None
    status: Optional[str] = None
    output: Any = None
    usage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ModelResponse":
        data = dict(payload)
        return cls(
            request_id=_coerce_str(data.get("request_id") or data.get("requestId") or data.get("id")),
            model_id=_coerce_str(data.get("model_id") or data.get("modelId") or data.get("model")),
            status=_coerce_str(data.get("status") or data.get("state")),
            output=data.get("output") if "output" in data else data.get("result"),
            usage=_normalize_mapping(data.get("usage") or data.get("metrics")),
            metadata=_normalize_mapping(data.get("metadata") or data.get("meta")),
            error=_coerce_str(data.get("error") or data.get("message")),
        )

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.request_id is not None:
            payload["request_id"] = self.request_id
        if self.model_id is not None:
            payload["model_id"] = self.model_id
        if self.status is not None:
            payload["status"] = self.status
        if self.output is not None:
            payload["output"] = self.output
        if self.usage:
            payload["usage"] = dict(self.usage)
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        if self.error is not None:
            payload["error"] = self.error
        return payload


@dataclass(slots=True)
class NormalizedModelRecord:
    model_id: Optional[str] = None
    name: Optional[str] = None
    provider: Optional[str] = None
    version: Optional[str] = None
    enabled: Optional[bool] = None
    context_window: Optional[int] = None
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "NormalizedModelRecord":
        data = dict(payload)
        return cls(
            model_id=_coerce_str(data.get("model_id") or data.get("modelId") or data.get("id")),
            name=_coerce_str(data.get("name") or data.get("label") or data.get("title")),
            provider=_coerce_str(data.get("provider") or data.get("vendor") or data.get("source")),
            version=_coerce_str(data.get("version") or data.get("model_version") or data.get("modelVersion")),
            enabled=_coerce_bool(data.get("enabled") or data.get("active")),
            context_window=_coerce_int(data.get("context_window") or data.get("contextWindow") or data.get("window")),
            max_output_tokens=_coerce_int(data.get("max_output_tokens") or data.get("maxOutputTokens") or data.get("max_tokens")),
            temperature=_coerce_float(data.get("temperature") or data.get("temp")),
            metadata=_normalize_mapping(data.get("metadata") or data.get("meta") or data.get("attributes")),
        )

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.model_id is not None:
            payload["model_id"] = self.model_id
        if self.name is not None:
            payload["name"] = self.name
        if self.provider is not None:
            payload["provider"] = self.provider
        if self.version is not None:
            payload["version"] = self.version
        if self.enabled is not None:
            payload["enabled"] = self.enabled
        if self.context_window is not None:
            payload["context_window"] = self.context_window
        if self.max_output_tokens is not None:
            payload["max_output_tokens"] = self.max_output_tokens
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


def normalize_request(payload: Mapping[str, Any]) -> ModelRequest:
    return ModelRequest.from_payload(payload)


def normalize_response(payload: Mapping[str, Any]) -> ModelResponse:
    return ModelResponse.from_payload(payload)


def normalize_model_record(payload: Mapping[str, Any]) -> NormalizedModelRecord:
    return NormalizedModelRecord.from_payload(payload)
