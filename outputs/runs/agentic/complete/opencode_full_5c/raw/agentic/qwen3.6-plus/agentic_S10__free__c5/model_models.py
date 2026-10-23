import os
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class LLMRequest:
    messages: list[dict[str, str]]
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    stream: bool = False
    stop: Optional[list[str]] = None
    response_format: Optional[dict[str, str]] = None
    tools: Optional[list[dict[str, Any]]] = None


@dataclass
class LLMResponse:
    content: str
    model: str
    finish_reason: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    role: str = "assistant"


@dataclass
class StreamChunk:
    delta: str
    index: int
    finish_reason: Optional[str] = None


@dataclass
class EmbeddingRequest:
    input: str | list[str]
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None
    encoding_format: str = "float"


@dataclass
class EmbeddingResponse:
    embeddings: list[list[float]]
    model: str
    total_tokens: int = 0


@dataclass
class ModerationRequest:
    input: str | list[str]
    model: str = "omni-moderation-latest"


@dataclass
class ModerationResult:
    flagged: bool
    categories: dict[str, bool] = field(default_factory=dict)
    category_scores: dict[str, float] = field(default_factory=dict)


@dataclass
class ModerationResponse:
    results: list[ModerationResult]
    model: str


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    model: str = "gpt-4o"
    source_language: Optional[str] = None
    temperature: float = 0.3


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    model: str


@dataclass
class SpokenBriefRequest:
    text: str
    voice: str = "alloy"
    model: str = "tts-1"
    speed: float = 1.0
    response_format: str = "mp3"


@dataclass
class SpokenBriefResponse:
    audio_data: bytes
    content_type: str
    model: str
    voice: str


@dataclass
class ModelConfig:
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    default_model: str = "gpt-4o"
    default_temperature: float = 0.7
    default_max_tokens: Optional[int] = None
    timeout: int = 60
    max_retries: int = 3

    @classmethod
    def from_env(cls) -> "ModelConfig":
        return cls(
            api_key=os.environ.get("OPENAI_API_KEY", ""),
            base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            default_model=os.environ.get("OPENAI_DEFAULT_MODEL", "gpt-4o"),
            default_temperature=float(
                os.environ.get("OPENAI_DEFAULT_TEMPERATURE", "0.7")
            ),
            default_max_tokens=int(os.environ["OPENAI_DEFAULT_MAX_TOKENS"])
            if os.environ.get("OPENAI_DEFAULT_MAX_TOKENS")
            else None,
            timeout=int(os.environ.get("OPENAI_TIMEOUT", "60")),
            max_retries=int(os.environ.get("OPENAI_MAX_RETRIES", "3")),
        )

    def to_client_kwargs(self) -> dict:
        return {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
        }


def normalize_messages(
    user_content: str, system_prompt: Optional[str] = None
) -> list[dict[str, str]]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_content})
    return messages


def parse_llm_response(raw_response) -> LLMResponse:
    choice = raw_response.choices[0]
    usage = raw_response.usage
    return LLMResponse(
        content=choice.message.content or "",
        model=raw_response.model,
        finish_reason=choice.finish_reason,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        role=choice.message.role or "assistant",
    )


def parse_stream_chunk(raw_chunk) -> Optional[StreamChunk]:
    if not raw_chunk.choices:
        return None
    choice = raw_chunk.choices[0]
    delta = choice.delta
    if delta is None or delta.content is None:
        return None
    return StreamChunk(
        delta=delta.content,
        index=choice.index,
        finish_reason=choice.finish_reason,
    )


def parse_moderation_response(raw_response) -> ModerationResponse:
    results = []
    for r in raw_response.results:
        results.append(
            ModerationResult(
                flagged=r.flagged,
                categories=dict(r.categories),
                category_scores=dict(r.category_scores),
            )
        )
    return ModerationResponse(
        results=results,
        model=raw_response.model,
    )


def parse_embedding_response(raw_response) -> EmbeddingResponse:
    embeddings = [item.embedding for item in raw_response.data]
    return EmbeddingResponse(
        embeddings=embeddings,
        model=raw_response.model,
        total_tokens=raw_response.usage.total_tokens if raw_response.usage else 0,
    )
