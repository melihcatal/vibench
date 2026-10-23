from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


def _normalize_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    text = str(value).strip().lower()
    return text in {"1", "true", "yes", "y", "on"}


def _normalize_int(value: Any, default: int = 0) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _normalize_float(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_mapping(value: Any) -> Dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _normalize_sequence_of_strings(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [_normalize_str(value)] if value.strip() else []
    if isinstance(value, Sequence):
        return [_normalize_str(item) for item in value if _normalize_str(item)]
    return []


@dataclass
class ManagedModelRequest:
    model_id: str
    input_text: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ManagedModelRequest":
        return cls(
            model_id=_normalize_str(payload.get("model_id") or payload.get("modelId")),
            input_text=_normalize_str(payload.get("input_text") or payload.get("inputText") or payload.get("prompt")),
            parameters=_normalize_mapping(payload.get("parameters") or payload.get("params")),
            metadata=_normalize_mapping(payload.get("metadata")),
        )

    def to_payload(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "input_text": self.input_text,
            "parameters": dict(self.parameters),
            "metadata": dict(self.metadata),
        }

    def normalize(self) -> "ManagedModelRequest":
        self.model_id = _normalize_str(self.model_id)
        self.input_text = _normalize_str(self.input_text)
        self.parameters = _normalize_mapping(self.parameters)
        self.metadata = _normalize_mapping(self.metadata)
        return self


@dataclass
class ManagedModelResponse:
    request_id: str = ""
    model_id: str = ""
    output_text: str = ""
    raw_output: Any = None
    usage: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = ""
    success: bool = False

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ManagedModelResponse":
        return cls(
            request_id=_normalize_str(payload.get("request_id") or payload.get("requestId") or payload.get("id")),
            model_id=_normalize_str(payload.get("model_id") or payload.get("modelId") or payload.get("model")),
            output_text=_normalize_str(payload.get("output_text") or payload.get("outputText") or payload.get("text") or payload.get("response")),
            raw_output=payload.get("raw_output") or payload.get("rawOutput") or payload.get("data"),
            usage=_normalize_mapping(payload.get("usage")),
            metadata=_normalize_mapping(payload.get("metadata")),
            status=_normalize_str(payload.get("status")),
            success=_normalize_bool(payload.get("success", payload.get("ok"))),
        )

    def to_payload(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "model_id": self.model_id,
            "output_text": self.output_text,
            "raw_output": self.raw_output,
            "usage": dict(self.usage),
            "metadata": dict(self.metadata),
            "status": self.status,
            "success": self.success,
        }

    def normalize(self) -> "ManagedModelResponse":
        self.request_id = _normalize_str(self.request_id)
        self.model_id = _normalize_str(self.model_id)
        self.output_text = _normalize_str(self.output_text)
        self.usage = _normalize_mapping(self.usage)
        self.metadata = _normalize_mapping(self.metadata)
        self.status = _normalize_str(self.status)
        self.success = _normalize_bool(self.success)
        return self


@dataclass
class ManagedModelNormalization:
    request: ManagedModelRequest
    response: ManagedModelResponse
    tags: List[str] = field(default_factory=list)
    temperature: float = 0.0
    retries: int = 0
    enabled: bool = True

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ManagedModelNormalization":
        request_payload = _normalize_mapping(payload.get("request"))
        response_payload = _normalize_mapping(payload.get("response"))
        return cls(
            request=ManagedModelRequest.from_payload(request_payload),
            response=ManagedModelResponse.from_payload(response_payload),
            tags=_normalize_sequence_of_strings(payload.get("tags")),
            temperature=_normalize_float(payload.get("temperature")),
            retries=_normalize_int(payload.get("retries")),
            enabled=_normalize_bool(payload.get("enabled", True)),
        )

    def to_payload(self) -> Dict[str, Any]:
        return {
            "request": self.request.to_payload(),
            "response": self.response.to_payload(),
            "tags": list(self.tags),
            "temperature": self.temperature,
            "retries": self.retries,
            "enabled": self.enabled,
        }

    def normalize(self) -> "ManagedModelNormalization":
        self.request.normalize()
        self.response.normalize()
        self.tags = _normalize_sequence_of_strings(self.tags)
        self.temperature = _normalize_float(self.temperature)
        self.retries = _normalize_int(self.retries)
        self.enabled = _normalize_bool(self.enabled)
        return self
