"""Local request, response, and normalization helpers for Managed Model Platform Workflow.

Defines data models for platform invocation requests, responses,
metadata collection, and downstream processing outputs.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformInvocationRequest:
    """Standardized request for invoking a managed model platform.

    Attributes:
        prompt: User prompt or message content.
        system_prompt: Optional system-level instructions.
        model: Provider-specific model identifier or deployment name.
        temperature: Sampling temperature (0.0 to 2.0).
        max_tokens: Maximum tokens to generate.
        top_p: Nucleus sampling parameter.
        extra_params: Provider-specific additional parameters.
    """

    prompt: str
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def to_openai_messages(self) -> List[Dict[str, str]]:
        """Convert to OpenAI chat completion message format.

        Returns:
            List of message dictionaries for the OpenAI API.
        """
        messages: List[Dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.prompt})
        return messages

    def to_anthropic_messages(self) -> List[Dict[str, Any]]:
        """Convert to Anthropic Messages API format.

        Returns:
            Tuple of (system_prompt, messages_list) for Anthropic API.
        """
        system = self.system_prompt or None
        messages: List[Dict[str, Any]] = [
            {"role": "user", "content": self.prompt}
        ]
        return system, messages


@dataclass
class PlatformInvocationResponse:
    """Standardized response from a managed model platform invocation.

    Attributes:
        text: Generated text content.
        model: Model identifier that produced the output.
        response_id: Platform-specific response/request ID.
        usage: Token usage statistics.
        raw_response: Original provider response object.
        provider: Provider identifier.
    """

    text: str
    model: str
    response_id: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    raw_response: Any = None
    provider: str = "openai"

    @property
    def total_tokens(self) -> Optional[int]:
        """Return total token count if available."""
        if self.usage and "total_tokens" in self.usage:
            return self.usage["total_tokens"]
        return None


@dataclass
class PlatformMetadata:
    """Provider platform metadata returned alongside model output.

    Attributes:
        response_id: Unique identifier for the platform response.
        model_id: Concrete model identifier used.
        deployment_id: Provider deployment or inference profile ID.
        usage: Token usage breakdown.
        finish_reason: Reason the generation stopped.
        created_at: Response timestamp.
        provider: Provider identifier.
        raw_metadata: Full raw metadata from the provider.
    """

    response_id: Optional[str] = None
    model_id: Optional[str] = None
    deployment_id: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    finish_reason: Optional[str] = None
    created_at: Optional[int] = None
    provider: str = "openai"
    raw_metadata: Optional[Dict[str, Any]] = None


@dataclass
class StreamingChunk:
    """Represents a single chunk from a streaming platform response.

    Attributes:
        text: Text delta in this chunk.
        index: Choice index in multi-choice responses.
        finish_reason: Finish reason if this is the final chunk.
        raw_chunk: Original provider chunk object.
    """

    text: str
    index: int = 0
    finish_reason: Optional[str] = None
    raw_chunk: Any = None


@dataclass
class SafetyCheckResult:
    """Result from platform output safety evaluation.

    Attributes:
        is_safe: Whether the content passed safety checks.
        categories: Dictionary of safety category flags.
        category_scores: Dictionary of confidence scores per category.
        flagged_categories: List of categories that triggered flags.
        raw_response: Original moderation response.
    """

    is_safe: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    flagged_categories: List[str] = field(default_factory=list)
    raw_response: Any = None


@dataclass
class LocalizationResult:
    """Result from platform output localization.

    Attributes:
        original_text: Original text before translation.
        translated_text: Translated text content.
        source_locale: Detected or specified source locale code.
        target_locale: Target locale code.
        provider: Translation provider identifier.
    """

    original_text: str
    translated_text: str
    source_locale: str = "en"
    target_locale: str = "en"
    provider: str = "deepl"


@dataclass
class EmbeddingResult:
    """Result from platform output embedding generation.

    Attributes:
        text: Input text that was embedded.
        embedding: Vector representation of the text.
        model: Embedding model identifier.
        dimensions: Dimensionality of the embedding vector.
        provider: Embedding provider identifier.
    """

    text: str
    embedding: List[float]
    model: str = "text-embedding-3-small"
    dimensions: int = 1536
    provider: str = "openai"


@dataclass
class AudioBriefingResult:
    """Result from spoken briefing generation.

    Attributes:
        text: Input text that was converted to speech.
        audio_data: Raw audio bytes.
        audio_format: Audio format (e.g., "mp3", "opus").
        model: TTS model identifier.
        voice: Voice identifier used.
        provider: Audio generation provider.
    """

    text: str
    audio_data: bytes
    audio_format: str = "mp3"
    model: str = "tts-1-hd"
    voice: str = "alloy"
    provider: str = "openai"


def build_platform_request(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    **kwargs: Any,
) -> PlatformInvocationRequest:
    """Factory function to create a platform invocation request.

    Args:
        prompt: User prompt text.
        system_prompt: Optional system prompt.
        model: Model identifier override.
        **kwargs: Additional parameters passed to PlatformInvocationRequest.

    Returns:
        Configured PlatformInvocationRequest instance.
    """
    return PlatformInvocationRequest(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        **kwargs,
    )


def normalize_safety_result(
    moderation_response: Any, provider: str = "openai"
) -> SafetyCheckResult:
    """Normalize a provider safety/moderation response into SafetyCheckResult.

    Args:
        moderation_response: Raw moderation API response.
        provider: Provider identifier.

    Returns:
        Normalized SafetyCheckResult.
    """
    result = moderation_response.results[0]
    categories = {}
    category_scores = {}
    flagged = []

    if hasattr(result, "categories"):
        for cat, flagged_val in result.categories.model_dump().items():
            categories[cat] = flagged_val
            if flagged_val:
                flagged.append(cat)

    if hasattr(result, "category_scores"):
        category_scores = result.category_scores.model_dump()

    return SafetyCheckResult(
        is_safe=len(flagged) == 0,
        categories=categories,
        category_scores=category_scores,
        flagged_categories=flagged,
        raw_response=moderation_response,
    )
