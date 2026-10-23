from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from openai.types.chat import ChatCompletion


@dataclass
class PlatformRequest:
    """Request for platform model invocation."""

    user_message: str
    system_prompt: str = "You are a helpful assistant."
    temperature: float = 0.7
    max_tokens: int = 1000
    model_id: Optional[str] = None
    additional_params: Dict[str, Any] = field(default_factory=dict)

    def to_openai_messages(self) -> list:
        """Convert to OpenAI message format."""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.user_message})
        return messages


@dataclass
class PlatformResponse:
    """Response from platform model invocation."""

    content: str
    model_id: str
    usage: Optional[Any] = None
    raw_response: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_token_counts(self) -> Dict[str, int]:
        """Extract token counts from usage."""
        if not self.usage:
            return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        if hasattr(self.usage, "prompt_tokens"):
            return {
                "prompt_tokens": self.usage.prompt_tokens,
                "completion_tokens": self.usage.completion_tokens,
                "total_tokens": self.usage.total_tokens,
            }
        return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    def is_successful(self) -> bool:
        """Check if response was successful."""
        return bool(self.content) and len(self.content) > 0


@dataclass
class PlatformStreamChunk:
    """Chunk from streaming response."""

    content: str
    is_complete: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_openai_response(response: ChatCompletion) -> PlatformResponse:
    """Normalize OpenAI response to PlatformResponse."""
    return PlatformResponse(
        content=response.choices[0].message.content,
        model_id=response.model,
        usage=response.usage,
        raw_response=response,
    )
