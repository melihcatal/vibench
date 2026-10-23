from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


def _first_present(data: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and data[key] is not None:
            return data[key]
    return None


def _as_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {}


@dataclass
class ModelRequest:
    model: str
    input: Any
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ModelRequest":
        return cls(
            model=str(_first_present(payload, "model", "model_id", "deployment", "deployment_id") or ""),
            input=_first_present(payload, "input", "prompt", "messages", "data"),
            parameters=_as_dict(_first_present(payload, "parameters", "params", "options")),
            metadata=_as_dict(_first_present(payload, "metadata", "meta", "context")),
        )

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"model": self.model, "input": self.input}
        if self.parameters:
            payload["parameters"] = dict(self.parameters)
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass
class ModelResponse:
    id: str
    model: str
    output: Any
    status: str = "succeeded"
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ModelResponse":
        return cls(
            id=str(_first_present(payload, "id", "request_id", "response_id") or ""),
            model=str(_first_present(payload, "model", "model_id", "deployment", "deployment_id") or ""),
            output=_first_present(payload, "output", "result", "data", "choices"),
            status=str(_first_present(payload, "status", "state") or "succeeded"),
            usage=_as_dict(_first_present(payload, "usage", "token_usage", "metrics")),
            raw=dict(payload),
        )

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "id": self.id,
            "model": self.model,
            "output": self.output,
            "status": self.status,
        }
        if self.usage:
            payload["usage"] = dict(self.usage)
        if self.raw:
            payload["raw"] = dict(self.raw)
        return payload


def normalize_request(payload: Mapping[str, Any]) -> ModelRequest:
    return ModelRequest.from_payload(payload)


def normalize_response(payload: Mapping[str, Any]) -> ModelResponse:
    return ModelResponse.from_payload(payload)


def normalize_workflow(payload: Mapping[str, Any]) -> Dict[str, Any]:
    request = normalize_request(_as_dict(_first_present(payload, "request", "input", "task", "job")))
    response_payload = _as_dict(_first_present(payload, "response", "result", "output"))
    response = normalize_response(response_payload) if response_payload else None
    workflow: Dict[str, Any] = {
        "request": request.to_payload(),
        "response": response.to_payload() if response else None,
        "status": str(_first_present(payload, "status", "state") or (response.status if response else "pending")),
        "metadata": _as_dict(_first_present(payload, "metadata", "meta", "context")),
    }
    return workflow
