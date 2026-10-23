"""
Local request, response, and normalization helpers for Managed Model Platform Workflow.

Provides Pydantic-style dataclasses for normalizing Amazon Bedrock
request payloads, response parsing, and metadata extraction.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PlatformRequest:
    """Normalized request payload for Amazon Bedrock platform invocation.

    Provider-specific: designed around Bedrock Converse API structure.
    """
    model_id: str
    messages: list[dict]
    system_prompt: Optional[str] = None
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    stop_sequences: Optional[list[str]] = None

    def to_bedrock_payload(self) -> dict:
        """Convert to Amazon Bedrock Converse API format.

        Provider-specific: uses Bedrock's `modelId`, `messages`, `system`,
        and `inferenceConfig` schema.
        """
        payload = {
            "modelId": self.model_id,
            "messages": self.messages,
            "inferenceConfig": {
                "maxTokens": self.max_tokens,
                "temperature": self.temperature,
                "topP": self.top_p,
            },
        }
        if self.system_prompt:
            payload["system"] = [{"text": self.system_prompt}]
        if self.stop_sequences:
            payload["inferenceConfig"]["stopSequences"] = self.stop_sequences
        return payload


@dataclass
class PlatformResponse:
    """Normalized response from Amazon Bedrock platform invocation.

    Captures the generated text and stop reason from Bedrock's response format.
    """
    output_text: str = ""
    stop_reason: Optional[str] = None
    role: str = "assistant"

    @classmethod
    def from_bedrock_response(cls, response: dict) -> "PlatformResponse":
        """Parse an Amazon Bedrock Converse API response dict.

        Provider-specific: extracts from Bedrock's `output.message.content[0].text`
        and `stopReason` fields.
        """
        output_text = ""
        stop_reason = response.get("stopReason")

        output_block = response.get("output", {})
        message_block = output_block.get("message", {})
        content_list = message_block.get("content", [])
        for item in content_list:
            if "text" in item:
                output_text += item["text"]

        return cls(
            output_text=output_text,
            stop_reason=stop_reason,
            role=message_block.get("role", "assistant"),
        )


@dataclass
class PlatformMetadata:
    """Metadata extracted from Amazon Bedrock platform responses.

    Provider-specific: captures Bedrock usage tokens, latency, and
    model ID from the platform response envelope.
    """
    model_id: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    stop_reason: Optional[str] = None
    latency_ms: float = 0.0
    request_id: str = ""

    @classmethod
    def from_bedrock_response(cls, response: dict) -> "PlatformMetadata":
        """Extract metadata from an Amazon Bedrock Converse API response.

        Provider-specific: reads Bedrock's `usage` block with
        `inputTokens`, `outputTokens`, `totalTokens`, plus ResponseMetadata.
        """
        usage = response.get("usage", {})
        response_metadata = response.get("ResponseMetadata", {})

        return cls(
            model_id=response.get("modelId", ""),
            input_tokens=usage.get("inputTokens", 0),
            output_tokens=usage.get("outputTokens", 0),
            total_tokens=usage.get("totalTokens", 0),
            stop_reason=response.get("stopReason"),
            request_id=response_metadata.get("RequestId", ""),
        )


@dataclass
class StreamedChunk:
    """A single streamed chunk from Amazon Bedrock ConverseStream.

    Provider-specific: maps to Bedrock streaming event types
    (messageStart, contentBlockStart, contentBlockDelta, contentBlockStop,
    messageStop, metadata).
    """
    chunk_type: str = ""
    text: str = ""
    index: int = 0
    stop_reason: Optional[str] = None
    usage: Optional[dict] = field(default_factory=dict)


def parse_stream_event(event: dict) -> Optional[StreamedChunk]:
    """Parse a single Amazon Bedrock ConverseStream event into a StreamedChunk.

    Provider-specific: handles Bedrock's streaming response event schema
    with event types like messageStart, contentBlockDelta, messageStop, metadata.
    """
    if not event:
        return None

    if "messageStart" in event:
        return StreamedChunk(
            chunk_type="messageStart",
            role=event["messageStart"].get("role", "assistant"),
        )

    if "contentBlockStart" in event:
        return StreamedChunk(
            chunk_type="contentBlockStart",
            index=event["contentBlockStart"].get("contentBlockIndex", 0),
        )

    if "contentBlockDelta" in event:
        delta = event["contentBlockDelta"].get("delta", {})
        return StreamedChunk(
            chunk_type="contentBlockDelta",
            text=delta.get("text", ""),
            index=event["contentBlockDelta"].get("contentBlockIndex", 0),
        )

    if "contentBlockStop" in event:
        return StreamedChunk(
            chunk_type="contentBlockStop",
            index=event["contentBlockStop"].get("contentBlockIndex", 0),
        )

    if "messageStop" in event:
        return StreamedChunk(
            chunk_type="messageStop",
            stop_reason=event["messageStop"].get("stopReason"),
        )

    if "metadata" in event:
        return StreamedChunk(
            chunk_type="metadata",
            usage=event["metadata"].get("usage", {}),
        )

    return None


def collect_streamed_text(chunks: list[StreamedChunk]) -> str:
    """Collect all text from a list of StreamedChunk objects.

    Aggregates contentBlockDelta text in order.
    """
    text_parts = []
    for chunk in sorted(chunks, key=lambda c: (c.index, c.chunk_type)):
        if chunk.chunk_type == "contentBlockDelta" and chunk.text:
            text_parts.append(chunk.text)
    return "".join(text_parts)


def build_user_message(content: str) -> dict:
    """Build a Bedrock-format user message dict.

    Provider-specific: returns {"role": "user", "content": [{"text": ...}]}.
    """
    return {"role": "user", "content": [{"text": content}]}


def build_assistant_message(content: str) -> dict:
    """Build a Bedrock-format assistant message dict.

    Provider-specific: returns {"role": "assistant", "content": [{"text": ...}]}.
    """
    return {"role": "assistant", "content": [{"text": content}]}
