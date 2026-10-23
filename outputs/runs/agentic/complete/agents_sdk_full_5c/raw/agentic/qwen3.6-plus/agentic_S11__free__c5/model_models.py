"""
Define local request, response, and normalization helpers for Managed Model Platform Workflow.

Provides Pydantic models and dataclasses for structured interaction
with the Azure OpenAI managed model platform, including request payloads,
response wrappers, and metadata carriers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PlatformModelRequest:
    """
    Request payload for invoking a managed model on the Azure OpenAI platform.

    Attributes:
        deployment_name: Azure OpenAI deployment name (e.g., gpt-4o, gpt-35-turbo).
        system_prompt: Optional system-level instruction for the model.
        user_content: Required user message content.
        temperature: Sampling temperature (0.0 to 2.0).
        max_tokens: Maximum number of tokens to generate.
        top_p: Nucleus sampling parameter.
        stop: Optional sequence at which generation stops.
    """
    deployment_name: str
    user_content: str
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    stop: Optional[list[str]] = None
    extra_body: Optional[dict[str, Any]] = None


@dataclass
class PlatformModelResponse:
    """
    Wrapped response from an Azure OpenAI managed model invocation.

    Attributes:
        content: Generated text content from the model.
        model_id: Azure OpenAI model identifier returned in the response.
        deployment_name: Deployment name that was invoked.
        request_id: Unique request identifier from Azure OpenAI.
        finish_reason: Reason generation stopped (e.g., 'stop', 'length').
        usage: Token usage statistics.
        raw_response: Full raw response object from the Azure OpenAI SDK.
    """
    content: str
    model_id: str
    deployment_name: str
    request_id: Optional[str] = None
    finish_reason: Optional[str] = None
    usage: dict[str, int] = field(default_factory=dict)
    raw_response: Optional[Any] = None


@dataclass
class PlatformMetadata:
    """
    Platform metadata carrier for Azure OpenAI responses.

    Collects resource identifiers, usage data, and model handles
    returned by the Azure OpenAI service.

    Attributes:
        model_id: The model identifier from the response.
        deployment_name: Azure OpenAI deployment name used.
        created_timestamp: Unix timestamp of response creation.
        system_fingerprint: System fingerprint for reproducibility tracking.
        prompt_tokens: Number of tokens in the prompt.
        completion_tokens: Number of tokens in the completion.
        total_tokens: Total tokens used.
        content_filter_results: Azure content filter results if available.
        resource_region: Azure region of the resource.
    """
    model_id: str
    deployment_name: str
    created_timestamp: Optional[int] = None
    system_fingerprint: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    content_filter_results: Optional[dict[str, Any]] = None
    resource_region: Optional[str] = None


@dataclass
class StreamingChunk:
    """
    Individual chunk from a streaming Azure OpenAI response.

    Attributes:
        content: Text delta from this chunk.
        finish_reason: None until the final chunk.
        index: Choice index for this chunk.
        raw_delta: Raw delta object from the Azure OpenAI stream.
    """
    content: str
    finish_reason: Optional[str] = None
    index: int = 0
    raw_delta: Optional[Any] = None


@dataclass
class EmbeddingResult:
    """
    Result from an Azure OpenAI embedding operation.

    Attributes:
        embedding: Vector embedding as a list of floats.
        model_id: Embedding model identifier.
        deployment_name: Azure OpenAI embedding deployment name.
        usage: Token usage for the embedding request.
        raw_response: Full raw response object.
    """
    embedding: list[float]
    model_id: str
    deployment_name: str
    usage: dict[str, int] = field(default_factory=dict)
    raw_response: Optional[Any] = None


@dataclass
class SpeechResult:
    """
    Result from an Azure OpenAI text-to-speech operation.

    Attributes:
        audio_data: Binary audio content.
        model_id: TTS model identifier used.
        deployment_name: Azure OpenAI TTS deployment name.
        voice_name: Voice name used for speech generation.
        format: Audio format (e.g., 'mp3', 'wav').
        raw_response: Full raw response object.
    """
    audio_data: bytes
    model_id: str
    deployment_name: str
    voice_name: str
    format: str
    raw_response: Optional[Any] = None


@dataclass
class SafetyCheckResult:
    """
    Result from content safety analysis via Azure AI Content Safety.

    Attributes:
        is_safe: Whether the content passed all safety checks.
        severity_scores: Category-level severity scores from Azure.
        categories: Content categories evaluated.
        blocklist_match: Whether content matched a blocklist.
        raw_response: Full raw response from Azure AI Content Safety.
    """
    is_safe: bool
    severity_scores: dict[str, float] = field(default_factory=dict)
    categories: list[str] = field(default_factory=list)
    blocklist_match: bool = False
    raw_response: Optional[Any] = None


@dataclass
class TranslatedOutput:
    """
    Translated output from a locale translation operation.

    Attributes:
        translated_content: Content translated to target locale.
        source_locale: Detected or specified source locale.
        target_locale: Target locale code.
        model_id: Model used for translation.
        deployment_name: Azure OpenAI deployment used.
        raw_response: Full raw response object.
    """
    translated_content: str
    source_locale: Optional[str]
    target_locale: str
    model_id: str
    deployment_name: str
    raw_response: Optional[Any] = None
