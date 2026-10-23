from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


@dataclass
class ModelRequest:
    prompt: str
    model_id: str
    max_tokens: int = 100
    temperature: float = 0.7
    top_p: float = 0.9
    stop_sequences: List[str] = None

    def __post_init__(self):
        if self.stop_sequences is None:
            self.stop_sequences = ["\n\nHuman:"]

    def to_bedrock_format(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "max_tokens_to_sample": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stop_sequences": self.stop_sequences,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelRequest":
        return cls(
            prompt=data.get("prompt", ""),
            model_id=data.get("model_id", "anthropic.claude-v2"),
            max_tokens=data.get("max_tokens", 100),
            temperature=data.get("temperature", 0.7),
            top_p=data.get("top_p", 0.9),
            stop_sequences=data.get("stop_sequences", ["\n\nHuman:"]),
        )


@dataclass
class ModelResponse:
    completion: str
    model_id: str
    request_id: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    raw_response: Optional[Dict[str, Any]] = None

    @classmethod
    def from_bedrock_response(
        cls, response: Dict[str, Any], model_id: str, request_id: str = None
    ) -> "ModelResponse":
        completion = response.get("completion", "")
        usage = response.get("usage")

        return cls(
            completion=completion,
            model_id=model_id,
            request_id=request_id,
            usage=usage,
            raw_response=response,
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "completion": self.completion,
            "model_id": self.model_id,
            "request_id": self.request_id,
        }

        if self.usage:
            result["usage"] = self.usage

        return result


@dataclass
class ModelMetadata:
    model_id: str
    invocation_timestamp: datetime
    latency_ms: int
    http_status_code: int
    request_id: str
    response_headers: Dict[str, str]
    usage: Optional[Dict[str, int]] = None
    invocation_metrics: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "invocation_timestamp": self.invocation_timestamp.isoformat(),
            "latency_ms": self.latency_ms,
            "http_status_code": self.http_status_code,
            "request_id": self.request_id,
            "response_headers": self.response_headers,
            "usage": self.usage,
            "invocation_metrics": self.invocation_metrics,
        }


def normalize_bedrock_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize different Bedrock model response formats.
    """
    normalized = {}

    if "completion" in response_data:
        normalized["text"] = response_data["completion"]
        normalized["type"] = "completion"
    elif "output" in response_data:
        normalized["text"] = response_data["output"]
        normalized["type"] = "output"
    elif "generations" in response_data:
        if response_data["generations"]:
            normalized["text"] = response_data["generations"][0].get("text", "")
            normalized["type"] = "generation"

    if "usage" in response_data:
        normalized["usage"] = response_data["usage"]

    return normalized


def create_error_response(error: Exception, model_id: str) -> ModelResponse:
    return ModelResponse(
        completion=f"Error: {str(error)}",
        model_id=model_id,
        raw_response={"error": str(error)},
    )
