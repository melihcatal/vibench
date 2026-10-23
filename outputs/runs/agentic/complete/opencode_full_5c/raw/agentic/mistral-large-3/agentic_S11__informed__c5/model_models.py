from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field


class VertexModelRequest(BaseModel):
    """Request model for Vertex AI managed model invocations."""

    prompt: str
    max_output_tokens: Optional[int] = Field(
        default=1024, description="Maximum number of tokens to generate"
    )
    temperature: Optional[float] = Field(
        default=0.9, description="Sampling temperature"
    )
    top_p: Optional[float] = Field(
        default=1.0, description="Nucleus sampling probability"
    )
    top_k: Optional[int] = Field(default=40, description="Top-k sampling")


class VertexModelResponse(BaseModel):
    """Response model for Vertex AI managed model invocations."""

    predictions: List[Dict[str, Any]]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    model_version: Optional[str] = None
    usage: Optional[Dict[str, int]] = None


class VertexChatMessage(BaseModel):
    """Message model for Vertex AI chat invocations."""

    author: str
    content: str


class VertexChatRequest(BaseModel):
    """Request model for Vertex AI chat invocations."""

    messages: List[VertexChatMessage]
    max_output_tokens: Optional[int] = Field(
        default=1024, description="Maximum number of tokens to generate"
    )
    temperature: Optional[float] = Field(
        default=0.9, description="Sampling temperature"
    )
    top_p: Optional[float] = Field(
        default=1.0, description="Nucleus sampling probability"
    )
    top_k: Optional[int] = Field(default=40, description="Top-k sampling")


def normalize_vertex_response(response: Dict[str, Any]) -> VertexModelResponse:
    """Normalizes a Vertex AI response into a standardized format."""
    return VertexModelResponse(
        predictions=response.get("predictions", []),
        metadata=response.get("metadata", {}),
        model_version=response.get("modelVersionId"),
        usage=response.get("metadata", {}).get("usage"),
    )
