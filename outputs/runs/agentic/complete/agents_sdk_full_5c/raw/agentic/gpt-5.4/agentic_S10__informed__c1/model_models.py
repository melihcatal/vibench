from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class ChatTurn:
    role: str
    content: str

    def as_openai(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass(slots=True)
class GenerationOptions:
    model: str
    temperature: float = 0.2
    max_tokens: int = 400
    top_p: Optional[float] = None
    response_format: Optional[Dict[str, Any]] = None

    def as_kwargs(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if self.top_p is not None:
            data["top_p"] = self.top_p
        if self.response_format is not None:
            data["response_format"] = self.response_format
        return data


@dataclass(slots=True)
class NormalizedLLMResult:
    text: str
    model: str
    finish_reason: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


def normalize_chat_response(response: Any) -> NormalizedLLMResult:
    choice = response.choices[0]
    message = getattr(choice, "message", None)
    text = getattr(message, "content", "") if message is not None else ""
    usage_obj = getattr(response, "usage", None)
    usage = {}
    if usage_obj is not None:
        for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
            value = getattr(usage_obj, key, None)
            if value is not None:
                usage[key] = value
    return NormalizedLLMResult(
        text=text or "",
        model=getattr(response, "model", ""),
        finish_reason=getattr(choice, "finish_reason", None),
        usage=usage,
        raw=response,
    )


def build_messages(system_prompt: str, user_prompt: str, extra_turns: Optional[List[ChatTurn]] = None) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
    if extra_turns:
        messages.extend(turn.as_openai() for turn in extra_turns)
    messages.append({"role": "user", "content": user_prompt})
    return messages
