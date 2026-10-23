from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal, Union
import json


# ---------------------------------------------------------------------------
# Normalized request payload model
# ---------------------------------------------------------------------------
class LLMRequest(BaseModel):
    model: str = Field(..., description="Identifier of the model family to use")
    messages: List[Dict[str, Any]] = Field(
        ..., description="List of message objects (role/content pairs)"
    )
    temperature: float = Field(0.0, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(
        1024, ge=1, le=8192, description="Maximum tokens to generate"
    )
    top_p: float = Field(1.0, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    n: int = Field(1, ge=1, description="Number of completions to return")
    stream: bool = Field(False, description="Whether to stream partial outputs")

    class Config:
        extra = "allow"  # allow additional vendor‑specific fields


# ---------------------------------------------------------------------------
# Normalized response model
# ---------------------------------------------------------------------------
class LLMChoice(BaseModel):
    index: int = Field(..., description="Index of the completion within the batch")
    message: Dict[str, Any] = Field(..., description="Generated message object")
    finish_reason: str = Field(..., description="Why generation stopped")
    logprobs: Dict[str, Any] = Field(None, description="Optional log‑probabilities")


class LLMResponse(BaseModel):
    id: str = Field(..., description="Unique ID for the request/response")
    object: Literal["chat.completion"] = "chat.completion"
    created: int = Field(..., description="Unix timestamp of generation")
    model: str = Field(..., description="Model that fulfilled the request")
    choices: List[LLMChoice] = Field(..., description="Generated completions")
    usage: Dict[str, int] = Field(..., description="Token usage counters")

    class Config:
        arbitrary_types_allowed = True


# ---------------------------------------------------------------------------
# Helper to flatten a raw provider response into our canonical shape
# ---------------------------------------------------------------------------
def normalize(raw: Any) -> LLMResponse:
    """Translate a vendor‑specific response into LLMResponse.

    Vendors often wrap data under different keys (e.g., `choices`, `data`, `output`).
    This function normalizes them into a unified contract used by the integration
    modules.
    """
    # Example: OpenAI structure
    if hasattr(raw, "choices"):
        choices = [choice for choice in raw.choices if choice]
        return LLMResponse(
            id=raw.id,
            created=raw.created,
            model=raw.model,
            choices=[
                {
                    "index": c.index,
                    "message": c.message,
                    "finish_reason": c.finish_reason,
                    "logprobs": getattr(c, "logprobs", None),
                }
                for c in choices
            ],
            usage=raw.usage,
        )
    # Add more adapters for other providers here
    raise ValueError("Unsupported provider response format")
