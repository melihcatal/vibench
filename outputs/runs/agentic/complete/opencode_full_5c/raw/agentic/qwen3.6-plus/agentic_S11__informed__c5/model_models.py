import os
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ModelRequest:
    prompt: str
    model: str = "qwen-plus"
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.8
    stream: bool = False
    system_prompt: Optional[str] = None
    extra_params: dict = field(default_factory=dict)


@dataclass
class ModelResponse:
    content: str
    model: str
    request_id: str
    finish_reason: str
    usage: dict = field(default_factory=dict)
    raw_response: Optional[Any] = None


@dataclass
class StreamChunk:
    content: str
    index: int
    finish_reason: Optional[str]
    raw_chunk: Optional[Any] = None


@dataclass
class PlatformMetadata:
    model_id: str
    request_id: str
    usage_input_tokens: int
    usage_output_tokens: int
    usage_total_tokens: int
    finish_reason: str
    latency_ms: Optional[float] = None
    resource_id: Optional[str] = None
    raw_response: Optional[Any] = None


@dataclass
class SafetyResult:
    text: str
    is_safe: bool
    categories: dict
    risk_level: str
    raw_response: Optional[Any] = None


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    raw_response: Optional[Any] = None


@dataclass
class EmbeddingResult:
    text: str
    embedding: list
    model: str
    token_count: int
    raw_response: Optional[Any] = None


@dataclass
class AudioResult:
    text: str
    audio_data: bytes
    audio_format: str
    model: str
    raw_response: Optional[Any] = None


@dataclass
class ResourceInfo:
    model_id: str
    model_name: str
    model_family: str
    status: str
    capabilities: list
    max_input_tokens: int
    max_output_tokens: int
    raw_response: Optional[Any] = None
