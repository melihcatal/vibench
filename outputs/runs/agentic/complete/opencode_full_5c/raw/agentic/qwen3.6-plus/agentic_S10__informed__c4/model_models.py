from dataclasses import dataclass, field
from typing import Any


@dataclass
class LLMRequest:
    model: str
    messages: list[dict[str, str]]
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    stream: bool = False
    response_format: dict[str, str] | None = None

    def to_openai_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "stream": self.stream,
        }
        if self.response_format:
            kwargs["response_format"] = self.response_format
        return kwargs


@dataclass
class LLMResponse:
    content: str
    model: str
    finish_reason: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    @classmethod
    def from_openai(cls, response: Any) -> "LLMResponse":
        choice = response.choices[0]
        usage = response.usage
        return cls(
            content=choice.message.content.strip(),
            model=response.model,
            finish_reason=choice.finish_reason,
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
        )


@dataclass
class StreamChunk:
    content: str
    finish_reason: str | None = None


def normalize_messages(
    system_prompt: str,
    user_prompt: str,
    context: str | None = None,
) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": system_prompt},
    ]
    if context:
        messages.append({"role": "user", "content": f"Context:\n{context}"})
    messages.append({"role": "user", "content": user_prompt})
    return messages
