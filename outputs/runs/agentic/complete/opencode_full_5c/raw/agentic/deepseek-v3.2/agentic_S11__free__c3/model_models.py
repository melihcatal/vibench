from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class ChatRequest:
    """Normalized chat request structure."""

    messages: List[Dict[str, str]]
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        payload = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
        }

        if self.max_tokens:
            payload["max_tokens"] = self.max_tokens
        if self.stream:
            payload["stream"] = self.stream

        return payload


@dataclass
class ChatResponse:
    """Normalized chat response structure."""

    content: str
    model: str
    usage: Optional[Dict[str, int]]
    raw_response: Any

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "content": self.content,
            "model": self.model,
            "usage": self.usage,
            "provider": "openai",
        }


class ModelMetadata(BaseModel):
    """Metadata about model capabilities."""

    provider: str
    model_id: str
    max_tokens: int
    supports_streaming: bool
    supports_function_calling: bool

    @classmethod
    def from_openai_model(cls, model_id: str) -> "ModelMetadata":
        """Create metadata from OpenAI model ID."""
        # Map known OpenAI models to their capabilities
        capabilities = {
            "gpt-4o": {"max_tokens": 16384, "supports_function_calling": True},
            "gpt-4o-2024-08-06": {
                "max_tokens": 128000,
                "supports_function_calling": True,
            },
            "gpt-4-turbo": {"max_tokens": 128000, "supports_function_calling": True},
            "gpt-3.5-turbo": {"max_tokens": 16384, "supports_function_calling": True},
        }

        default_caps = {"max_tokens": 4096, "supports_function_calling": False}
        caps = capabilities.get(model_id, default_caps)

        return cls(
            provider="openai",
            model_id=model_id,
            max_tokens=caps["max_tokens"],
            supports_streaming=True,
            supports_function_calling=caps["supports_function_calling"],
        )


def normalize_openai_response(openai_response) -> ChatResponse:
    """Normalize OpenAI response to standard format."""
    return ChatResponse(
        content=openai_response.choices[0].message.content,
        model=openai_response.model,
        usage={
            "prompt_tokens": openai_response.usage.prompt_tokens,
            "completion_tokens": openai_response.usage.completion_tokens,
            "total_tokens": openai_response.usage.total_tokens,
        },
        raw_response=openai_response,
    )
