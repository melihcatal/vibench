from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    prompt: str = Field(..., description="Input prompt for the LLM")
    system_prompt: Optional[str] = Field(
        default=None, description="System-level instructions for the LLM"
    )
    max_tokens: Optional[int] = Field(
        default=None, description="Override for max tokens in response"
    )
    temperature: Optional[float] = Field(
        default=None, description="Override for model temperature"
    )


class LLMResponse(BaseModel):
    content: str = Field(..., description="Generated text from the LLM")
    model: str = Field(..., description="Model identifier used for generation")
    stop_reason: Optional[str] = Field(
        default=None, description="Reason for stopping generation"
    )
    usage: Optional[Dict[str, int]] = Field(
        default=None, description="Token usage statistics"
    )


def normalize_request(request: Union[Dict[str, Any], LLMRequest]) -> LLMRequest:
    """Normalize raw request data into a structured LLMRequest."""
    if isinstance(request, dict):
        return LLMRequest(**request)
    return request


def normalize_response(response: Dict[str, Any], model_id: str) -> LLMResponse:
    """Normalize raw response data into a structured LLMResponse."""
    if "content" in response and isinstance(response["content"], list):
        content = "".join(
            [item["text"] for item in response["content"] if item["type"] == "text"]
        )
    else:
        content = response.get("content", "")

    return LLMResponse(
        content=content,
        model=model_id,
        stop_reason=response.get("stop_reason"),
        usage=response.get("usage"),
    )
