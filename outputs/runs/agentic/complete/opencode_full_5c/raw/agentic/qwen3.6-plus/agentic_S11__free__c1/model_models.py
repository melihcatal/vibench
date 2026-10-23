from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PlatformModelRequest:
    model_id: str
    prompt: str
    system_prompt: Optional[str] = None
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    stop_sequences: Optional[list[str]] = None
    inference_profile_arn: Optional[str] = None
    deployment_id: Optional[str] = None


@dataclass
class PlatformModelResponse:
    text: str
    model_id: str
    stop_reason: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    request_id: Optional[str] = None
    resource_arn: Optional[str] = None
    latency_ms: Optional[float] = None
    raw_response: Optional[dict[str, Any]] = None


@dataclass
class StreamChunk:
    text: str
    index: int
    is_final: bool = False
    raw_chunk: Optional[dict[str, Any]] = None


@dataclass
class PlatformStreamResponse:
    chunks: list[StreamChunk] = field(default_factory=list)
    model_id: str = ""
    stop_reason: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    request_id: Optional[str] = None
    resource_arn: Optional[str] = None
    raw_response: Optional[dict[str, Any]] = None


@dataclass
class SafetyCheckResult:
    is_safe: bool
    flagged_categories: list[str] = field(default_factory=list)
    confidence_scores: dict[str, float] = field(default_factory=dict)
    raw_assessment: Optional[dict[str, Any]] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    raw_response: Optional[dict[str, Any]] = None


@dataclass
class EmbeddingResult:
    embedding: list[float]
    model_id: str
    input_tokens: int = 0
    raw_response: Optional[dict[str, Any]] = None


@dataclass
class AudioResult:
    audio_stream: bytes
    content_type: str
    duration_ms: Optional[float] = None
    raw_response: Optional[dict[str, Any]] = None


@dataclass
class ModelResource:
    model_id: str
    model_arn: str
    provider: str
    model_family: str
    supported_modalities: list[str] = field(default_factory=list)
    max_input_tokens: int = 0
    max_output_tokens: int = 0


def normalize_bedrock_response(
    response: dict[str, Any], model_id: str
) -> PlatformModelResponse:
    output = response.get("output", {})
    message = output.get("message", {})
    content_blocks = message.get("content", [])
    text_parts = []
    for block in content_blocks:
        if block.get("type") == "text":
            text_parts.append(block.get("text", ""))
    text = "".join(text_parts)
    stop_reason = message.get("stopReason", "end_turn")
    usage = response.get("usage", {})
    input_tokens = usage.get("inputTokens", 0)
    output_tokens = usage.get("outputTokens", 0)
    total_tokens = usage.get("totalTokens", input_tokens + output_tokens)
    return PlatformModelResponse(
        text=text,
        model_id=model_id,
        stop_reason=stop_reason,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        raw_response=response,
    )


def normalize_bedrock_stream_usage(usage: dict[str, Any]) -> dict[str, int]:
    return {
        "input_tokens": usage.get("inputTokens", 0),
        "output_tokens": usage.get("outputTokens", 0),
        "total_tokens": usage.get("totalTokens", 0),
    }


def build_bedrock_converse_payload(request: PlatformModelRequest) -> dict[str, Any]:
    messages = [{"role": "user", "content": [{"text": request.prompt}]}]
    inference_config = {
        "maxTokens": request.max_tokens,
        "temperature": request.temperature,
        "topP": request.top_p,
    }
    if request.stop_sequences:
        inference_config["stopSequences"] = request.stop_sequences
    payload: dict[str, Any] = {
        "modelId": request.model_id,
        "messages": messages,
        "inferenceConfig": inference_config,
    }
    if request.system_prompt:
        payload["system"] = [{"text": request.system_prompt}]
    return payload
