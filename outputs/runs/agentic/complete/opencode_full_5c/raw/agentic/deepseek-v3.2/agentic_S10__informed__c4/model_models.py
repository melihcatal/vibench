from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class ModelProvider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    AWS = "aws"


@dataclass
class CompletionRequest:
    """Request for model completion."""

    messages: List[Dict[str, str]]
    max_tokens: int = 1000
    temperature: float = 0.7
    top_p: Optional[float] = None
    stream: bool = False

    def to_anthropic_format(self) -> Dict[str, Any]:
        """Convert to Anthropic API format."""
        return {
            "messages": self.messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        return {
            "messages": self.messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": self.stream,
        }


@dataclass
class CompletionResponse:
    """Response from model completion."""

    text: str
    model: str
    usage: Optional[Dict[str, int]] = None
    finish_reason: Optional[str] = None

    @classmethod
    def from_anthropic(cls, response: Any, model: str) -> "CompletionResponse":
        """Create from Anthropic response."""
        return cls(
            text=response.content[0].text,
            model=model,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }
            if hasattr(response, "usage")
            else None,
            finish_reason=response.stop_reason
            if hasattr(response, "stop_reason")
            else None,
        )

    @classmethod
    def from_openai(cls, response: Any, model: str) -> "CompletionResponse":
        """Create from OpenAI response."""
        return cls(
            text=response.choices[0].message.content,
            model=model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
            if hasattr(response, "usage")
            else None,
            finish_reason=response.choices[0].finish_reason
            if hasattr(response.choices[0], "finish_reason")
            else None,
        )


def normalize_messages(
    messages: List[Dict[str, str]], provider: ModelProvider
) -> List[Dict[str, str]]:
    """Normalize messages for different providers."""
    normalized = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")

        # Anthropic uses "assistant" role, OpenAI uses "assistant"
        if provider == ModelProvider.ANTHROPIC:
            if role == "system":
                # Anthropic handles system messages differently
                continue
            normalized.append({"role": role, "content": content})
        else:
            normalized.append({"role": role, "content": content})

    return normalized


def create_user_message(content: str) -> Dict[str, str]:
    """Create a user message."""
    return {"role": "user", "content": content}


def create_assistant_message(content: str) -> Dict[str, str]:
    """Create an assistant message."""
    return {"role": "assistant", "content": content}


def create_system_message(content: str) -> Dict[str, str]:
    """Create a system message."""
    return {"role": "system", "content": content}
