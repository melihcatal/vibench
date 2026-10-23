"""Local request, response, and normalization helpers for Managed Model Platform Workflow.

Provider: Amazon Bedrock via boto3
Defines dataclasses for Bedrock inference requests, responses, and metadata normalization.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformModelRequest:
    """Normalized request payload for Amazon Bedrock model invocation.

    Maps to the Anthropic Claude message format used by
    anthropic.claude-3-sonnet-20240229-v1:0 on Bedrock.
    """
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    system_prompt: str = ""
    messages: List[Dict[str, Any]] = field(default_factory=list)
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: Optional[int] = None

    def to_bedrock_payload(self) -> bytes:
        """Serialize to the JSON body expected by Bedrock's InvokeModel API."""
        body: Dict[str, Any] = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": self.max_tokens,
            "messages": self.messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }
        if self.system_prompt:
            body["system"] = [{"type": "text", "text": self.system_prompt}]
        if self.top_k is not None:
            body["top_k"] = self.top_k
        return json.dumps(body).encode("utf-8")

    @classmethod
    def from_text(
        cls,
        text: str,
        model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
        system_prompt: str = "",
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> "PlatformModelRequest":
        """Build a request from a single user text prompt."""
        return cls(
            model_id=model_id,
            system_prompt=system_prompt,
            messages=[{"role": "user", "content": [{"type": "text", "text": text}]}],
            max_tokens=max_tokens,
            temperature=temperature,
        )


@dataclass
class PlatformModelResponse:
    """Normalized response from Amazon Bedrock model invocation.

    Captures the generated text and provider metadata such as
    input/output token counts, model ID, and stop reason.
    """
    generated_text: str
    model_id: str
    stop_reason: str
    input_tokens: int
    output_tokens: int
    raw_response: Dict[str, Any] = field(default_factory=dict)
    usage_metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_bedrock_response(
        cls, response_body: Dict[str, Any], model_id: str, raw_response: Optional[Dict[str, Any]] = None
    ) -> "PlatformModelResponse":
        """Parse a Bedrock Claude response dict into a normalized response."""
        content_blocks = response_body.get("content", [])
        generated_text = ""
        for block in content_blocks:
            if block.get("type") == "text":
                generated_text += block.get("text", "")
        usage = response_body.get("usage", {})
        return cls(
            generated_text=generated_text,
            model_id=model_id,
            stop_reason=response_body.get("stop_reason", "unknown"),
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            raw_response=raw_response or response_body,
            usage_metadata=usage,
        )


@dataclass
class StreamChunk:
    """A single chunk from a streamed Bedrock response."""
    text: str
    delta_json: Dict[str, Any]
    is_complete: bool = False


@dataclass
class SafetyResult:
    """Result from Amazon Comprehend toxic content detection."""
    is_safe: bool
    scores: Dict[str, float]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    """Result from Amazon Translate."""
    translated_text: str
    source_language: str
    target_language: str
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    """Result from Amazon Titan Embeddings via Bedrock."""
    vector: List[float]
    input_tokens: int
    model_id: str
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AudioResult:
    """Result from Amazon Polly TTS synthesis."""
    audio_bytes: bytes
    content_type: str
    raw_response: Dict[str, Any] = field(default_factory=dict)


def build_messages_from_text(text: str) -> List[Dict[str, Any]]:
    """Build a Claude-compatible messages list from plain text."""
    return [{"role": "user", "content": [{"type": "text", "text": text}]}]


def extract_text_from_bedrock_response(response_body: Dict[str, Any]) -> str:
    """Extract concatenated text from a Bedrock Claude response body."""
    parts: List[str] = []
    for block in response_body.get("content", []):
        if block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "".join(parts)
