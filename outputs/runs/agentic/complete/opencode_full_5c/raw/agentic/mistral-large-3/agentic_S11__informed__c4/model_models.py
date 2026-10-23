from typing import Dict, Any, Optional, TypedDict, List
from pydantic import BaseModel


class ModelRequest(BaseModel):
    prompt: str
    parameters: Optional[Dict[str, Any]] = None


class ModelResponse(BaseModel):
    results: List[Dict[str, Any]]
    model_id: str
    provider: str
    metadata: Optional[Dict[str, Any]] = None


class StreamChunk(TypedDict):
    chunk: str
    metadata: Dict[str, Any]


def normalize_request(request: Dict[str, Any]) -> ModelRequest:
    return ModelRequest(**request)


def normalize_response(response: Dict[str, Any]) -> ModelResponse:
    return ModelResponse(
        results=response.get("results", []),
        model_id=response.get("model_id", "unknown"),
        provider=response.get("provider", "unknown"),
        metadata=response.get("metadata", {}),
    )
