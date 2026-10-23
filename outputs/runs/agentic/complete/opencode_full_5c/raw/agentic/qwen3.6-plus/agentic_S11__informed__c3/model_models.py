import os
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ModelRequest:
    prompt: str
    system_prompt: Optional[str] = None
    model_id: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.8
    stop_sequences: Optional[list[str]] = None
    stream: bool = False
    extra_params: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelResponse:
    text: str
    model_id: str
    finish_reason: Optional[str] = None
    usage: dict[str, Any] = field(default_factory=dict)
    request_id: Optional[str] = None
    raw_response: Optional[Any] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamChunk:
    text: str
    index: int
    finish_reason: Optional[str] = None
    raw_chunk: Optional[Any] = None


@dataclass
class SafetyResult:
    text: str
    is_safe: bool
    categories: dict[str, float] = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)
    raw_response: Optional[Any] = None
    provider: str = ""


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    provider: str = ""
    raw_response: Optional[Any] = None


@dataclass
class EmbeddingResult:
    text: str
    embedding: list[float]
    model_id: str
    dimensions: int = 0
    raw_response: Optional[Any] = None
    provider: str = ""


@dataclass
class AudioResult:
    text: str
    audio_url: Optional[str] = None
    audio_data: Optional[bytes] = None
    format: str = "mp3"
    model_id: str = ""
    raw_response: Optional[Any] = None
    provider: str = ""


def normalize_prompt(prompt: str) -> str:
    return prompt.strip()


def build_messages(
    system_prompt: Optional[str], user_prompt: str
) -> list[dict[str, str]]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    return messages


def extract_text_from_response(response: Any) -> str:
    if hasattr(response, "output") and hasattr(response.output, "text"):
        return response.output.text
    if hasattr(response, "output") and isinstance(response.output, dict):
        return response.output.get("text", "")
    if isinstance(response, dict):
        return response.get("output", {}).get("text", "")
    return str(response)


def extract_usage_from_response(response: Any) -> dict[str, Any]:
    if hasattr(response, "usage") and hasattr(response.usage, "input_tokens"):
        return {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
        }
    if hasattr(response, "usage") and isinstance(response.usage, dict):
        return response.usage
    if isinstance(response, dict):
        return response.get("usage", {})
    return {}


def extract_request_id(response: Any) -> Optional[str]:
    if hasattr(response, "request_id"):
        return response.request_id
    if isinstance(response, dict):
        return response.get("request_id")
    return None
