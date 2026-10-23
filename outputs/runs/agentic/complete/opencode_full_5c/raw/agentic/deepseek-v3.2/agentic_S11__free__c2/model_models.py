from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class ModelProvider(Enum):
    """Supported model providers."""

    OPENAI = "openai"
    # Add other providers as needed


@dataclass
class ChatMessage:
    """Represents a chat message in a conversation."""

    role: str  # "system", "user", "assistant"
    content: str

    def to_dict(self) -> Dict[str, str]:
        """Convert to provider-specific format."""
        return {"role": self.role, "content": self.content}


@dataclass
class ModelRequest:
    """Standardized model request structure."""

    messages: List[ChatMessage]
    model: str = "gpt-4o"
    max_tokens: int = 1000
    temperature: float = 0.7
    stream: bool = False

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        return {
            "model": self.model,
            "messages": [msg.to_dict() for msg in self.messages],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": self.stream,
        }


@dataclass
class ModelResponse:
    """Standardized model response structure."""

    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: str
    raw_response: Optional[Any] = None

    @classmethod
    def from_openai(cls, openai_response) -> "ModelResponse":
        """Create from OpenAI response object."""
        return cls(
            content=openai_response.choices[0].message.content,
            model=openai_response.model,
            usage={
                "prompt_tokens": openai_response.usage.prompt_tokens,
                "completion_tokens": openai_response.usage.completion_tokens,
                "total_tokens": openai_response.usage.total_tokens,
            },
            finish_reason=openai_response.choices[0].finish_reason,
            raw_response=openai_response,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "content": self.content,
            "model": self.model,
            "usage": self.usage,
            "finish_reason": self.finish_reason,
        }


def normalize_messages(messages: List[Dict[str, str]]) -> List[ChatMessage]:
    """Normalize messages from various formats to ChatMessage objects."""
    normalized = []
    for msg in messages:
        if isinstance(msg, ChatMessage):
            normalized.append(msg)
        elif isinstance(msg, dict) and "role" in msg and "content" in msg:
            normalized.append(ChatMessage(role=msg["role"], content=msg["content"]))
        else:
            raise ValueError(f"Invalid message format: {msg}")
    return normalized


def create_system_message(content: str) -> ChatMessage:
    """Create a system message."""
    return ChatMessage(role="system", content=content)


def create_user_message(content: str) -> ChatMessage:
    """Create a user message."""
    return ChatMessage(role="user", content=content)


def create_assistant_message(content: str) -> ChatMessage:
    """Create an assistant message."""
    return ChatMessage(role="assistant", content=content)
