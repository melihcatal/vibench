from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum


class ModelRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class PlatformMessage:
    role: str
    content: str

    def to_dashscope_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class PlatformRequest:
    model: str
    messages: list[PlatformMessage]
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.8
    stream: bool = False
    result_format: str = "message"

    def to_dashscope_payload(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "messages": [m.to_dashscope_dict() for m in self.messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "stream": self.stream,
            "result_format": self.result_format,
        }


@dataclass
class PlatformUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

    @classmethod
    def from_dashscope(cls, usage_dict: Optional[dict]) -> "PlatformUsage":
        if usage_dict is None:
            return cls()
        return cls(
            input_tokens=usage_dict.get("input_tokens", 0),
            output_tokens=usage_dict.get("output_tokens", 0),
            total_tokens=usage_dict.get("total_tokens", 0),
        )


@dataclass
class PlatformResponse:
    output_text: str
    model_id: str
    request_id: str
    usage: PlatformUsage
    finish_reason: str = ""
    raw_response: Optional[Any] = None

    @classmethod
    def from_dashscope(cls, response: Any) -> "PlatformResponse":
        output = response.output
        choices = output.get("choices", [])
        first_choice = choices[0] if choices else {}
        message = first_choice.get("message", {})

        usage_data = getattr(response, "usage", None)
        if isinstance(usage_data, dict):
            usage = PlatformUsage.from_dashscope(usage_data)
        else:
            usage = PlatformUsage()

        return cls(
            output_text=message.get("content", ""),
            model_id=getattr(response, "model", ""),
            request_id=getattr(response, "request_id", ""),
            usage=usage,
            finish_reason=first_choice.get("finish_reason", ""),
            raw_response=response,
        )


@dataclass
class PlatformStreamChunk:
    text_delta: str
    model_id: str
    request_id: str
    finish_reason: Optional[str] = None
    raw_chunk: Optional[Any] = None

    @classmethod
    def from_dashscope(cls, chunk: Any) -> "PlatformStreamChunk":
        output = chunk.output
        choices = output.get("choices", [])
        first_choice = choices[0] if choices else {}
        message = first_choice.get("message", {})
        return cls(
            text_delta=message.get("content", ""),
            model_id=getattr(chunk, "model", ""),
            request_id=getattr(chunk, "request_id", ""),
            finish_reason=first_choice.get("finish_reason"),
            raw_chunk=chunk,
        )


@dataclass
class SafetyResult:
    is_safe: bool
    categories: dict[str, bool] = field(default_factory=dict)
    scores: dict[str, float] = field(default_factory=dict)
    raw_response: Optional[Any] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    raw_response: Optional[Any] = None


@dataclass
class EmbeddingResult:
    embeddings: list[list[float]]
    model_id: str
    request_id: str
    usage: PlatformUsage = field(default_factory=PlatformUsage)
    raw_response: Optional[Any] = None


@dataclass
class AudioResult:
    audio_url: Optional[str] = None
    audio_data: Optional[bytes] = None
    model_id: str = ""
    request_id: str = ""
    raw_response: Optional[Any] = None
