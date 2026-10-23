from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class VertexAIRequest(BaseModel):
    prompt: str
    model_id: str = "gemini-1.5-pro-001"
    temperature: float = 0.7
    max_tokens: int = 1024


class VertexAIResponse(BaseModel):
    text: str
    metadata: Dict[str, Any]

    @classmethod
    def from_vertex_ai_response(cls, response: Any) -> "VertexAIResponse":
        return cls(
            text=response.text,
            metadata={
                "input_tokens": response._prediction_response.metadata.get("inputTokenCount", 0),
                "output_tokens": response._prediction_response.metadata.get("outputTokenCount", 0),
                "safety_ratings": response._prediction_response.metadata.get("safetyRatings", []),
            },
        )


class VertexAIStreamChunk(BaseModel):
    text: str
    metadata: Dict[str, Any]

    @classmethod
    def from_vertex_ai_stream(cls, response: Any) -> "VertexAIStreamChunk":
        return cls(
            text=response.outputs[0].text,
            metadata={
                "is_finished": response.outputs[0].is_finished,
            },
        )


class ModelResource(BaseModel):
    provider: str
    model_handle: str
    model_display_name: str
    metadata: Dict[str, Any]


class ModelOutputWithMetadata(BaseModel):
    output: str
    metadata: Dict[str, Any]