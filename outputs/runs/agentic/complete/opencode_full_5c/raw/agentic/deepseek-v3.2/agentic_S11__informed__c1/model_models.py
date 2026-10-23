from typing import Optional, Any, Dict
from dataclasses import dataclass
from pydantic import BaseModel, Field


@dataclass
class ChatRequest:
    """Request for chat completion."""

    user_message: str
    system_prompt: str = "You are a helpful AI assistant."
    temperature: float = 0.7
    max_tokens: int = 1000
    stream: bool = False


@dataclass
class ChatResponse:
    """Response from chat completion."""

    content: str
    finish_reason: Optional[str] = None
    raw_response: Optional[Any] = None


class NormalizedRequest(BaseModel):
    """Normalized request structure for different providers."""

    messages: list = Field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 1000
    stream: bool = False

    @classmethod
    def from_chat_request(cls, request: ChatRequest) -> "NormalizedRequest":
        """Convert ChatRequest to normalized format."""
        return cls(
            messages=[
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_message},
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream,
        )


class NormalizedResponse(BaseModel):
    """Normalized response structure from different providers."""

    content: str
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    model: Optional[str] = None

    @classmethod
    def from_azure_response(cls, response: Any) -> "NormalizedResponse":
        """Convert Azure OpenAI response to normalized format."""
        if hasattr(response, "choices") and response.choices:
            content = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
        else:
            content = ""
            finish_reason = None

        usage = None
        if hasattr(response, "usage") and response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

        model = getattr(response, "model", None)

        return cls(
            content=content, finish_reason=finish_reason, usage=usage, model=model
        )


def normalize_request(
    request: ChatRequest, provider: str = "azure-openai"
) -> Dict[str, Any]:
    """Normalize request for different providers."""
    normalized = NormalizedRequest.from_chat_request(request)

    # Provider-specific adjustments
    if provider == "azure-openai":
        return {
            "messages": normalized.messages,
            "temperature": normalized.temperature,
            "max_tokens": normalized.max_tokens,
            "stream": normalized.stream,
        }
    elif provider == "openai":
        return {
            "messages": normalized.messages,
            "temperature": normalized.temperature,
            "max_tokens": normalized.max_tokens,
            "stream": normalized.stream,
        }
    else:
        # Default to Azure OpenAI format
        return normalized.dict()
