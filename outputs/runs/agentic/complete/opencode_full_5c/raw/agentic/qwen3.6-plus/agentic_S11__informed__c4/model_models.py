from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class ModelRequest:
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    model_id: str = "qwen-turbo"
    top_p: float = 0.8
    stop_sequences: Optional[list] = None


@dataclass
class UsageInfo:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass
class ModelResponse:
    content: str
    model_id: str
    request_id: str
    usage: UsageInfo = field(default_factory=UsageInfo)
    finish_reason: Optional[str] = None


@dataclass
class StreamChunk:
    content: str
    finish_reason: Optional[str] = None
    index: int = 0


@dataclass
class StreamResponse:
    chunks: list = field(default_factory=list)
    model_id: str = ""
    request_id: str = ""
    usage: UsageInfo = field(default_factory=UsageInfo)

    @property
    def full_content(self) -> str:
        return "".join(chunk.content for chunk in self.chunks)


@dataclass
class MetadataResponse:
    output: str
    model_id: str
    request_id: str
    usage: UsageInfo = field(default_factory=UsageInfo)
    resource_id: Optional[str] = None
    model_handle: Optional[str] = None
    timestamp: Optional[datetime] = None
    raw_response: Optional[dict] = None


@dataclass
class SafetyCategory:
    name: str
    score: float
    is_violation: bool


@dataclass
class SafetyResult:
    is_safe: bool
    categories: list = field(default_factory=list)
    request_id: str = ""
    raw_response: Optional[dict] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    request_id: str = ""
    model_id: str = ""


@dataclass
class EmbeddingResult:
    embeddings: list
    model_id: str
    request_id: str
    usage: UsageInfo = field(default_factory=UsageInfo)


@dataclass
class AudioResult:
    audio_data: bytes
    format: str
    model_id: str
    request_id: str
    duration_ms: Optional[int] = None


def normalize_usage_from_dashscope(usage_dict: dict) -> UsageInfo:
    return UsageInfo(
        prompt_tokens=usage_dict.get("input_tokens", 0),
        completion_tokens=usage_dict.get("output_tokens", 0),
        total_tokens=usage_dict.get("total_tokens", 0),
    )


def normalize_messages(prompt: str, system_prompt: Optional[str] = None) -> list:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return messages


def build_dashscope_payload(request: ModelRequest) -> dict:
    payload = {
        "model": request.model_id,
        "input": {
            "messages": normalize_messages(request.prompt, request.system_prompt)
        },
        "parameters": {
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "top_p": request.top_p,
        },
    }
    if request.stop_sequences:
        payload["parameters"]["stop"] = request.stop_sequences
    return payload
