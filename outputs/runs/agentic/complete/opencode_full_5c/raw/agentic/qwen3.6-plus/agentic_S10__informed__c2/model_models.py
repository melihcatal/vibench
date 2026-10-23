from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class LLMRequest:
    model: str = "gpt-4o"
    system_prompt: Optional[str] = None
    user_prompt: Optional[str] = None
    messages: list[dict[str, str]] = field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    stream: bool = False
    json_mode: bool = False
    stop_sequences: Optional[list[str]] = None

    def to_messages(self) -> list[dict[str, str]]:
        if self.messages:
            return self.messages
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        if self.user_prompt:
            messages.append({"role": "user", "content": self.user_prompt})
        return messages

    def to_openai_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": self.to_messages(),
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "stream": self.stream,
        }
        if self.stop_sequences:
            kwargs["stop"] = self.stop_sequences
        if self.json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        return kwargs


@dataclass
class LLMResponse:
    content: str = ""
    model: str = ""
    finish_reason: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    raw_response: Optional[Any] = None


@dataclass
class StreamChunk:
    delta: str = ""
    finish_reason: Optional[str] = None
    index: int = 0


@dataclass
class SafetyResult:
    is_safe: bool = True
    categories: dict[str, float] = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)
    raw_response: Optional[Any] = None


@dataclass
class TranslationResult:
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    raw_response: Optional[Any] = None


@dataclass
class EmbeddingResult:
    embedding: list[float] = field(default_factory=list)
    model: str = ""
    usage: dict[str, int] = field(default_factory=dict)
    raw_response: Optional[Any] = None


@dataclass
class SpeechResult:
    audio_url: Optional[str] = None
    audio_bytes: Optional[bytes] = None
    content_type: str = "audio/mpeg"
    raw_response: Optional[Any] = None


def normalize_openai_response(response: Any) -> LLMResponse:
    choice = response.choices[0]
    usage = response.usage
    return LLMResponse(
        content=choice.message.content or "",
        model=response.model,
        finish_reason=choice.finish_reason,
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
        raw_response=response,
    )


def normalize_stream_chunk(chunk: Any) -> StreamChunk:
    choice = chunk.choices[0]
    delta = choice.delta
    return StreamChunk(
        delta=delta.content or "",
        finish_reason=choice.finish_reason,
        index=choice.index,
    )


def build_system_prompt(
    task_description: str,
    output_format: Optional[str] = None,
    constraints: Optional[list[str]] = None,
) -> str:
    parts = [task_description]
    if output_format:
        parts.append(f"Output format: {output_format}")
    if constraints:
        parts.append("Constraints:")
        for c in constraints:
            parts.append(f"- {c}")
    return "\n\n".join(parts)


def truncate_text(text: str, max_chars: int = 100000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[truncated]"
