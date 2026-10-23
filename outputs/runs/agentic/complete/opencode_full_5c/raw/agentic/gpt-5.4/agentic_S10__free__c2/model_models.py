from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChatMessage:
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class GenerationConfig:
    model: str
    temperature: float = 0.2
    max_output_tokens: int = 512
    top_p: float = 0.95


@dataclass
class PromptSafetyResult:
    provider: str
    model: str
    is_safe: bool
    categories: List[str] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict)
    flagged_segments: List[str] = field(default_factory=list)


@dataclass
class TextGenerationResult:
    provider: str
    model: str
    text: str
    finish_reason: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embedding: List[float]
    usage: Dict[str, Any] = field(default_factory=dict)


def normalize_messages(
    system_prompt: str, user_prompt: str, context: Optional[str] = None
) -> List[ChatMessage]:
    messages = [ChatMessage(role="system", content=system_prompt)]
    if context:
        messages.append(
            ChatMessage(
                role="user", content=f"Context:\n{context}\n\nRequest:\n{user_prompt}"
            )
        )
    else:
        messages.append(ChatMessage(role="user", content=user_prompt))
    return messages


def usage_to_dict(
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    total_tokens: Optional[int] = None,
) -> Dict[str, Any]:
    usage: Dict[str, Any] = {}
    if input_tokens is not None:
        usage["input_tokens"] = input_tokens
    if output_tokens is not None:
        usage["output_tokens"] = output_tokens
    if total_tokens is not None:
        usage["total_tokens"] = total_tokens
    return usage
