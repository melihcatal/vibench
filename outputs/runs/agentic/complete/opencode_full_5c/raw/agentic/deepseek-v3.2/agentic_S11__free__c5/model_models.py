from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


class Role(str, Enum):
    """Message roles for chat conversations."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    TOOL = "tool"


@dataclass
class Message:
    """A message in a chat conversation."""

    role: Role
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None


@dataclass
class ChatRequest:
    """Request for chat completion."""

    messages: List[Message]
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    tools: Optional[List[Dict]] = None
    tool_choice: Optional[str] = None

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        messages = []
        for msg in self.messages:
            message_dict = {"role": msg.role.value, "content": msg.content}
            if msg.name:
                message_dict["name"] = msg.name
            if msg.tool_calls:
                message_dict["tool_calls"] = msg.tool_calls
            if msg.tool_call_id:
                message_dict["tool_call_id"] = msg.tool_call_id
            messages.append(message_dict)

        request = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "stream": self.stream,
        }

        if self.max_tokens:
            request["max_tokens"] = self.max_tokens
        if self.tools:
            request["tools"] = self.tools
        if self.tool_choice:
            request["tool_choice"] = self.tool_choice

        return request


@dataclass
class Usage:
    """Token usage information."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    @classmethod
    def from_openai(cls, usage: Any) -> "Usage":
        """Create Usage from OpenAI usage object."""
        return cls(
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )


@dataclass
class ChatResponse:
    """Response from chat completion."""

    content: str
    model: str
    usage: Usage
    raw_response: Any = None
    finish_reason: Optional[str] = None
    id: Optional[str] = None
    created: Optional[int] = None

    @classmethod
    def from_openai(cls, response: Any) -> "ChatResponse":
        """Create ChatResponse from OpenAI response object."""
        return cls(
            content=response.choices[0].message.content,
            model=response.model,
            usage=Usage.from_openai(response.usage),
            raw_response=response,
            finish_reason=response.choices[0].finish_reason,
            id=response.id,
            created=response.created,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "content": self.content,
            "model": self.model,
            "usage": {
                "prompt_tokens": self.usage.prompt_tokens,
                "completion_tokens": self.usage.completion_tokens,
                "total_tokens": self.usage.total_tokens,
            },
            "finish_reason": self.finish_reason,
            "id": self.id,
            "created": self.created,
        }


@dataclass
class StreamChunk:
    """A chunk from a streaming response."""

    content: str
    model: str
    created: int
    id: str
    object_type: str

    @classmethod
    def from_openai_chunk(cls, chunk: Any) -> "StreamChunk":
        """Create StreamChunk from OpenAI streaming chunk."""
        return cls(
            content=chunk.choices[0].delta.content or "",
            model=chunk.model,
            created=chunk.created,
            id=chunk.id,
            object_type=chunk.object,
        )


def normalize_messages(messages: List[Dict]) -> List[Message]:
    """Normalize messages from various formats to Message objects."""
    normalized = []
    for msg in messages:
        if isinstance(msg, Message):
            normalized.append(msg)
        elif isinstance(msg, dict):
            role = Role(msg.get("role", "user"))
            normalized.append(
                Message(
                    role=role,
                    content=msg.get("content", ""),
                    name=msg.get("name"),
                    tool_calls=msg.get("tool_calls"),
                    tool_call_id=msg.get("tool_call_id"),
                )
            )
    return normalized


def create_system_message(content: str) -> Message:
    """Create a system message."""
    return Message(role=Role.SYSTEM, content=content)


def create_user_message(content: str, name: Optional[str] = None) -> Message:
    """Create a user message."""
    return Message(role=Role.USER, content=content, name=name)


def create_assistant_message(
    content: str, tool_calls: Optional[List[Dict]] = None
) -> Message:
    """Create an assistant message."""
    return Message(role=Role.ASSISTANT, content=content, tool_calls=tool_calls)
