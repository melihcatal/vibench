"""Define local request, response, and normalization helpers for Managed Model Platform Workflow.

Contains dataclasses for platform model requests/responses, utility functions for
normalizing Bedrock provider payloads, and metadata extraction helpers.
"""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformModelRequest:
    """Normalized request payload for platform model invocation."""
    prompt: str
    system_prompt: Optional[str] = None
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    stop_sequences: Optional[List[str]] = None
    stream: bool = False

    def to_bedrock_payload(self) -> dict:
        """Convert to Amazon Bedrock Anthropic Claude request format."""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.prompt})

        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "messages": messages,
        }
        if self.stop_sequences:
            payload["stop_sequences"] = self.stop_sequences
        return payload


@dataclass
class PlatformModelResponse:
    """Normalized response from platform model invocation."""
    text: str
    model_id: str
    stop_reason: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "model_id": self.model_id,
            "stop_reason": self.stop_reason,
            "usage": {
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "total_tokens": self.total_tokens,
            },
            "metadata": self.metadata,
        }


@dataclass
class StreamingChunk:
    """Represents a single chunk from a streaming generation."""
    text: str
    is_final: bool = False
    sequence_index: int = 0
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SafetyCheckResult:
    """Result from platform output safety analysis."""
    is_safe: bool
    flags: List[str] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResult:
    """Result from platform output translation."""
    translated_text: str
    source_language: str
    target_language: str
    confidence: float = 1.0
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingResult:
    """Result from platform output embedding."""
    embedding: List[float]
    input_tokens: int = 0
    model_id: str = ""
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AudioResult:
    """Result from text-to-speech synthesis."""
    audio_data: bytes
    content_type: str = "audio/mpeg"
    sample_rate: int = 22050
    metadata: Optional[Dict[str, Any]] = None


def parse_bedrock_response(
    response_body: dict,
    model_id: str,
) -> PlatformModelResponse:
    """Parse Amazon Bedrock Claude response into normalized format.

    Args:
        response_body: Parsed JSON from Bedrock invoke_model response.
        model_id: The model identifier used for invocation.

    Returns:
        Normalized PlatformModelResponse.
    """
    usage = response_body.get("usage", {})
    content_blocks = response_body.get("content", [])

    text_parts = []
    for block in content_blocks:
        if block.get("type") == "text":
            text_parts.append(block.get("text", ""))

    return PlatformModelResponse(
        text="\n".join(text_parts),
        model_id=model_id,
        stop_reason=response_body.get("stop_reason"),
        input_tokens=usage.get("input_tokens", 0),
        output_tokens=usage.get("output_tokens", 0),
        total_tokens=usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
        metadata={
            "stop_reason": response_body.get("stop_reason"),
            "model_id": model_id,
        },
    )


def parse_bedrock_stream_event(event: dict) -> Optional[StreamingChunk]:
    """Parse a Bedrock streaming event into a StreamingChunk.

    Handles content_block_delta, message_start, message_delta, and metadata events.

    Args:
        event: Parsed event dict from Bedrock streaming response.

    Returns:
        StreamingChunk or None for non-content events.
    """
    event_type = event.get("type")

    if event_type == "content_block_delta":
        delta = event.get("delta", {})
        text = delta.get("text", "")
        index = event.get("index", 0)
        if text:
            return StreamingChunk(
                text=text,
                is_final=False,
                sequence_index=index,
            )

    elif event_type == "message_delta":
        delta = event.get("delta", {})
        stop_reason = delta.get("stop_reason")
        if stop_reason:
            return StreamingChunk(
                text="",
                is_final=True,
                metadata={"stop_reason": stop_reason},
            )

    elif event_type == "metadata":
        usage = event.get("metadata", {}).get("usage", {})
        return StreamingChunk(
            text="",
            is_final=True,
            metadata={"usage": usage},
        )

    return None


def normalize_prompt_for_bedrock(prompt: str) -> str:
    """Ensure prompt meets Bedrock Claude formatting requirements."""
    stripped = prompt.strip()
    if not stripped:
        raise ValueError("Prompt cannot be empty")
    return stripped


def build_safety_payload(text: str) -> dict:
    """Build payload for Amazon Comprehend DetectToxicContent API.

    Args:
        text: Text to analyze for toxic content.

    Returns:
        Dict suitable for comprehend.detect_toxic_content().
    """
    return {"text": text, "language_code": "en"}


def build_translate_payload(
    text: str,
    source_lang: str = "auto",
    target_lang: str = "es",
) -> dict:
    """Build payload for Amazon Translate API.

    Args:
        text: Text to translate.
        source_lang: Source language code (auto for auto-detect).
        target_lang: Target language code.

    Returns:
        Dict suitable for translate.translate_text().
    """
    return {
        "text": text,
        "source_language_code": source_lang if source_lang != "auto" else "auto",
        "target_language_code": target_lang,
    }


def build_titan_embedding_payload(text: str) -> dict:
    """Build payload for Amazon Titan Embeddings model.

    Args:
        text: Text to embed.

    Returns:
        Dict suitable for Bedrock invoke_model with Titan embeddings.
    """
    return {"inputText": text}


def build_polly_payload(
    text: str,
    voice_id: str = "Joanna",
    output_format: str = "mp3",
) -> dict:
    """Build payload for Amazon Polly SynthesizeSpeech API.

    Args:
        text: Text to synthesize.
        voice_id: Polly voice identifier.
        output_format: Output audio format.

    Returns:
        Dict suitable for polly.synthesize_speech().
    """
    return {
        "Text": text,
        "VoiceId": voice_id,
        "OutputFormat": output_format,
    }
