from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    prompt: str = Field(..., description="Input prompt for the LLM")
    temperature: float = Field(0.7, description="Sampling temperature")
    max_tokens: int = Field(1000, description="Maximum number of tokens to generate")
    model_id: Optional[str] = Field(None, description="Override the default model ID")


class LLMResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the response")
    object: str = Field(..., description="Object type, e.g., 'chat.completion'")
    created: int = Field(..., description="Timestamp of the response")
    model: str = Field(..., description="Model identifier used for generation")
    choices: List[Dict[str, Any]] = Field(
        ..., description="List of generated completions"
    )
    usage: Dict[str, int] = Field(..., description="Token usage statistics")


class StreamChunk(BaseModel):
    id: str = Field(..., description="Unique identifier for the stream chunk")
    object: str = Field(..., description="Object type, e.g., 'chat.completion.chunk'")
    created: int = Field(..., description="Timestamp of the stream chunk")
    model: str = Field(..., description="Model identifier used for generation")
    choices: List[Dict[str, Any]] = Field(
        ..., description="List of streamed completions"
    )


def normalize_response(response: Dict[str, Any]) -> LLMResponse:
    """Normalize the raw response from the LLM service."""
    return LLMResponse(**response)


def normalize_stream_chunk(chunk: str) -> Optional[StreamChunk]:
    """Normalize a streamed chunk from the LLM service."""
    if not chunk.strip():
        return None
    try:
        data = chunk.split("data: ")[1]
        parsed = eval(data)  # Safely evaluate the chunk data
        return StreamChunk(**parsed)
    except (IndexError, SyntaxError, KeyError):
        return None
