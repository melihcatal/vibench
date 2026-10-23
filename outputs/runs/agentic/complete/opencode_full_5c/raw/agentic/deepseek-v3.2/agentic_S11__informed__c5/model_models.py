from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from openai.types.chat import ChatCompletion, ChatCompletionChunk


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ChatRequest:
    messages: List[ChatMessage]
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False


@dataclass
class ChatResponse:
    content: str
    model: str
    usage: Optional[Any] = None
    finish_reason: Optional[str] = None
    raw_response: Optional[ChatCompletion] = None


@dataclass
class StreamingChatResponse:
    content: str
    model: str
    finish_reason: Optional[str] = None
    raw_chunk: Optional[ChatCompletionChunk] = None


@dataclass
class PlatformMetadataResponse:
    content: str
    metadata: Dict[str, Any]
    raw_response: Optional[Any] = None


def normalize_chat_messages(messages: List[Dict[str, str]]) -> List[ChatMessage]:
    """
    Normalize chat messages from various formats.
    """
    normalized = []
    for msg in messages:
        if isinstance(msg, dict):
            normalized.append(
                ChatMessage(
                    role=msg.get("role", "user"), content=msg.get("content", "")
                )
            )
        elif isinstance(msg, ChatMessage):
            normalized.append(msg)
    return normalized


def create_system_message(content: str) -> ChatMessage:
    """
    Create a system message.
    """
    return ChatMessage(role="system", content=content)


def create_user_message(content: str) -> ChatMessage:
    """
    Create a user message.
    """
    return ChatMessage(role="user", content=content)


def create_assistant_message(content: str) -> ChatMessage:
    """
    Create an assistant message.
    """
    return ChatMessage(role="assistant", content=content)
