"""Define local request, response, and normalization helpers for Managed Model Platform Workflow."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class PlatformModelRequest:
    """Normalized request for invoking a platform-managed model."""
    model_id: str
    system_prompt: Optional[str] = None
    user_message: str = ""
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    stream: bool = False


@dataclass
class UsageInfo:
    """Token usage metadata from a provider response."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass
class PlatformModelResponse:
    """Normalized response from a platform model invocation."""
    generated_text: str = ""
    model_id: str = ""
    finish_reason: str = ""
    usage: UsageInfo = field(default_factory=UsageInfo)
    metadata: Dict[str, Any] = field(default_factory=dict)
    stop_reason: str = ""
    request_id: str = ""


@dataclass
class StreamChunk:
    """A single chunk from a streaming generation."""
    text: str = ""
    index: int = 0
    finish_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyCheckResult:
    """Result from a content safety check."""
    text: str = ""
    is_safe: bool = True
    labels: Dict[str, float] = field(default_factory=dict)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    flagged_categories: List[str] = field(default_factory=list)
    request_id: str = ""


@dataclass
class TranslationResult:
    """Result from a translation operation."""
    original_text: str = ""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    model_id: str = ""


@dataclass
class EmbeddingResult:
    """Result from an embedding operation."""
    text: str = ""
    embedding: List[float] = field(default_factory=list)
    model_id: str = ""
    token_count: int = 0
    dimensions: int = 0


@dataclass
class SpeechResult:
    """Result from a text-to-speech operation."""
    text: str = ""
    audio_content: bytes = b""
    voice_id: str = ""
    audio_format: str = ""
    sample_rate: int = 0


def normalize_bedrock_converse_usage(usage: Dict[str, Any]) -> UsageInfo:
    """Normalize Bedrock Converse API usage info into UsageInfo."""
    return UsageInfo(
        prompt_tokens=usage.get("inputTokens", 0),
        completion_tokens=usage.get("outputTokens", 0),
        total_tokens=usage.get("totalTokens", 0),
    )


def normalize_bedrock_response(
    response: Dict[str, Any],
    model_id: str,
) -> PlatformModelResponse:
    """Normalize a full Bedrock Converse response into PlatformModelResponse."""
    output = response.get("output", {})
    message = output.get("message", {})
    content_list = message.get("content", [])

    generated_text = ""
    for content_item in content_list:
        if "text" in content_item:
            generated_text = content_item["text"]

    stop_reason = response.get("stopReason", "")
    usage_raw = response.get("usage", {})

    return PlatformModelResponse(
        generated_text=generated_text,
        model_id=model_id,
        finish_reason=stop_reason,
        usage=normalize_bedrock_converse_usage(usage_raw),
        metadata={
            "ResponseMetadata": response.get("ResponseMetadata", {}),
            "stop_reason": stop_reason,
        },
        stop_reason=stop_reason,
        request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
    )


def build_bedrock_inference_config(
    max_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> Dict[str, Any]:
    """Build inference configuration dict for Bedrock Converse API."""
    return {
        "maxTokens": max_tokens,
        "temperature": temperature,
        "topP": top_p,
    }
