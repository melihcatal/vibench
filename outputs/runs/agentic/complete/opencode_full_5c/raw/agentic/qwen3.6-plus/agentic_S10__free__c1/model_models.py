import os
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class LLMRequest:
    model: str = "gpt-4o"
    prompt: str = ""
    system_prompt: str = ""
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 1.0
    stop: Optional[list[str]] = None
    seed: Optional[int] = None


@dataclass
class LLMResponse:
    text: str = ""
    model: str = ""
    finish_reason: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    raw: Optional[dict] = None


@dataclass
class SummarizeRequest:
    text: str = ""
    model: str = "gpt-4o-mini"
    max_length: int = 200
    temperature: float = 0.3


@dataclass
class SummarizeResponse:
    summary: str = ""
    original_length: int = 0
    summary_length: int = 0
    model: str = ""
    usage: dict = field(default_factory=dict)


@dataclass
class ExtractJsonRequest:
    text: str = ""
    schema_hint: str = ""
    model: str = "gpt-4o"
    temperature: float = 0.1


@dataclass
class ExtractJsonResponse:
    extracted: dict = field(default_factory=dict)
    raw_json: str = ""
    model: str = ""
    usage: dict = field(default_factory=dict)


@dataclass
class AnswerWithContextRequest:
    question: str = ""
    context: str = ""
    model: str = "gpt-4o"
    max_tokens: int = 512
    temperature: float = 0.5


@dataclass
class AnswerWithContextResponse:
    answer: str = ""
    cited_context: str = ""
    model: str = ""
    usage: dict = field(default_factory=dict)


@dataclass
class StreamRequest:
    prompt: str = ""
    system_prompt: str = ""
    model: str = "gpt-4o"
    max_tokens: int = 1024
    temperature: float = 0.7


@dataclass
class StreamChunk:
    delta: str = ""
    finish_reason: Optional[str] = None
    index: int = 0


@dataclass
class StreamResponse:
    full_text: str = ""
    chunks: list = field(default_factory=list)
    model: str = ""
    usage: dict = field(default_factory=dict)


@dataclass
class SafetyCheckRequest:
    text: str = ""
    model: str = "omni-moderation-latest"


@dataclass
class SafetyCheckResponse:
    flagged: bool = False
    categories: dict = field(default_factory=dict)
    category_scores: dict = field(default_factory=dict)
    model: str = ""
    raw: Optional[dict] = None


@dataclass
class TranslateRequest:
    text: str = ""
    target_language: str = "en"
    source_language: str = "auto"
    model: str = "gpt-4o-mini"
    temperature: float = 0.3


@dataclass
class TranslateResponse:
    translated_text: str = ""
    detected_language: str = ""
    target_language: str = ""
    model: str = ""
    usage: dict = field(default_factory=dict)


@dataclass
class EmbedRequest:
    texts: list[str] = field(default_factory=list)
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None


@dataclass
class EmbedResponse:
    embeddings: list[list[float]] = field(default_factory=list)
    model: str = ""
    usage: dict = field(default_factory=dict)


@dataclass
class SpokenBriefRequest:
    text: str = ""
    style: str = "conversational"
    max_words: int = 150
    model: str = "gpt-4o-mini"
    temperature: float = 0.5


@dataclass
class SpokenBriefResponse:
    brief: str = ""
    word_count: int = 0
    style: str = ""
    model: str = ""
    usage: dict = field(default_factory=dict)


def normalize_llm_request(req: LLMRequest) -> dict:
    messages = []
    if req.system_prompt:
        messages.append({"role": "system", "content": req.system_prompt})
    messages.append({"role": "user", "content": req.prompt})
    payload = {
        "model": req.model,
        "messages": messages,
        "max_tokens": req.max_tokens,
        "temperature": req.temperature,
        "top_p": req.top_p,
    }
    if req.stop:
        payload["stop"] = req.stop
    if req.seed is not None:
        payload["seed"] = req.seed
    return payload


def normalize_llm_response(raw: dict) -> LLMResponse:
    choice = raw.get("choices", [{}])[0]
    message = choice.get("message", {})
    usage = raw.get("usage", {})
    return LLMResponse(
        text=message.get("content", ""),
        model=raw.get("model", ""),
        finish_reason=choice.get("finish_reason", ""),
        prompt_tokens=usage.get("prompt_tokens", 0),
        completion_tokens=usage.get("completion_tokens", 0),
        total_tokens=usage.get("total_tokens", 0),
        raw=raw,
    )


def build_user_message(content: str) -> dict:
    return {"role": "user", "content": content}


def build_system_message(content: str) -> dict:
    return {"role": "system", "content": content}
