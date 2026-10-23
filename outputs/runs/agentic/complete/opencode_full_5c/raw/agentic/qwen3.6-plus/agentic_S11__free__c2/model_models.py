from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PlatformModelRequest:
    model: str
    messages: list[dict[str, str]]
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: Optional[list[str]] = None
    stream: bool = False
    response_format: Optional[dict[str, str]] = None
    tools: Optional[list[dict[str, Any]]] = None
    tool_choice: Optional[str] = None
    user: Optional[str] = None

    def to_openai_payload(self) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "stream": self.stream,
        }
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        if self.stop is not None:
            payload["stop"] = self.stop
        if self.response_format is not None:
            payload["response_format"] = self.response_format
        if self.tools is not None:
            payload["tools"] = self.tools
        if self.tool_choice is not None:
            payload["tool_choice"] = self.tool_choice
        if self.user is not None:
            payload["user"] = self.user
        return payload


@dataclass
class PlatformUsageInfo:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    completion_tokens_details: Optional[dict[str, int]] = None

    @classmethod
    def from_openai_usage(cls, usage) -> "PlatformUsageInfo":
        details = None
        if (
            hasattr(usage, "completion_tokens_details")
            and usage.completion_tokens_details
        ):
            details = {
                "reasoning_tokens": getattr(
                    usage.completion_tokens_details, "reasoning_tokens", 0
                ),
                "accepted_prediction_tokens": getattr(
                    usage.completion_tokens_details, "accepted_prediction_tokens", 0
                ),
                "rejected_prediction_tokens": getattr(
                    usage.completion_tokens_details, "rejected_prediction_tokens", 0
                ),
            }
        return cls(
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            completion_tokens_details=details,
        )


@dataclass
class PlatformModelResponse:
    content: str
    model: str
    finish_reason: str
    request_id: str
    usage: Optional[PlatformUsageInfo] = None
    system_fingerprint: Optional[str] = None
    created: Optional[int] = None
    raw_response: Optional[Any] = None

    @classmethod
    def from_openai_response(cls, response) -> "PlatformModelResponse":
        choice = response.choices[0]
        usage = None
        if response.usage:
            usage = PlatformUsageInfo.from_openai_usage(response.usage)
        return cls(
            content=choice.message.content or "",
            model=response.model,
            finish_reason=choice.finish_reason or "unknown",
            request_id=response.id,
            usage=usage,
            system_fingerprint=getattr(response, "system_fingerprint", None),
            created=getattr(response, "created", None),
            raw_response=response,
        )


@dataclass
class PlatformStreamChunk:
    delta_content: str
    finish_reason: Optional[str]
    request_id: str
    model: str
    raw_chunk: Optional[Any] = None

    @classmethod
    def from_openai_chunk(cls, chunk) -> "PlatformStreamChunk":
        choice = chunk.choices[0] if chunk.choices else None
        delta_content = ""
        finish_reason = None
        if choice:
            delta_content = choice.delta.content or ""
            finish_reason = choice.finish_reason
        return cls(
            delta_content=delta_content,
            finish_reason=finish_reason,
            request_id=chunk.id,
            model=chunk.model,
            raw_chunk=chunk,
        )


@dataclass
class PlatformResourceInfo:
    model_id: str
    model_family: str
    capabilities: list[str]
    is_available: bool = True
    deployment_name: Optional[str] = None
    region: Optional[str] = None

    @classmethod
    def from_openai_model_info(
        cls, model_id: str, info: dict
    ) -> "PlatformResourceInfo":
        return cls(
            model_id=model_id,
            model_family=info.get("family", "unknown"),
            capabilities=info.get("capabilities", []),
            is_available=True,
        )


@dataclass
class ModerationResult:
    flagged: bool
    categories: dict[str, bool] = field(default_factory=dict)
    category_scores: dict[str, float] = field(default_factory=dict)
    raw_result: Optional[Any] = None


@dataclass
class EmbeddingResult:
    embedding: list[float]
    model: str
    usage: Optional[PlatformUsageInfo] = None
    raw_result: Optional[Any] = None


@dataclass
class AudioResult:
    audio_bytes: bytes
    model: str
    format: str
    raw_result: Optional[Any] = None
