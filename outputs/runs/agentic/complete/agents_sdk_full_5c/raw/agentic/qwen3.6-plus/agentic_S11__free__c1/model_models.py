"""Define local request, response, and normalization helpers for Managed Model Platform Workflow.

This module provides Pydantic models and helper utilities for normalizing
requests and responses across the OpenAI managed model platform.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types import CreateEmbeddingResponse


@dataclass
class PlatformModelRequest:
    """Normalized request payload for invoking a managed model platform."""

    model_id: str
    messages: List[Dict[str, str]] = field(default_factory=list)
    temperature: float = 1.0
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    stream: bool = False
    stop: Optional[List[str]] = None

    def to_openai_payload(self) -> Dict[str, Any]:
        """Convert to OpenAI ChatCompletion create payload."""
        payload: Dict[str, Any] = {
            "model": self.model_id,
            "messages": self.messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": self.stream,
        }
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        if self.stop is not None:
            payload["stop"] = self.stop
        return payload


@dataclass
class PlatformModelResponse:
    """Normalized response from a managed model platform invocation."""

    content: str
    model_id: str
    finish_reason: Optional[str] = None
    usage_prompt_tokens: Optional[int] = None
    usage_completion_tokens: Optional[int] = None
    usage_total_tokens: Optional[int] = None
    response_id: Optional[str] = None
    created_timestamp: Optional[int] = None
    raw_response: Optional[Any] = None

    @classmethod
    def from_openai_completion(cls, completion: ChatCompletion) -> "PlatformModelResponse":
        """Build a normalized response from an OpenAI ChatCompletion object."""
        choice = completion.choices[0]
        usage = completion.usage
        message = choice.message

        content = message.content or ""
        return cls(
            content=content,
            model_id=completion.model,
            finish_reason=choice.finish_reason,
            usage_prompt_tokens=usage.prompt_tokens if usage else None,
            usage_completion_tokens=usage.completion_tokens if usage else None,
            usage_total_tokens=usage.total_tokens if usage else None,
            response_id=completion.id,
            created_timestamp=completion.created,
            raw_response=completion,
        )

    @classmethod
    def from_openai_chunks(cls, chunks: List[ChatCompletionChunk]) -> "PlatformModelResponse":
        """Build a normalized response from accumulated OpenAI streaming chunks."""
        if not chunks:
            return cls(content="", model_id="")

        accumulated_content = ""
        last_chunk = chunks[-1]
        model_id = last_chunk.model
        finish_reason = None
        usage_data = None

        for chunk in chunks:
            if chunk.choices:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    accumulated_content += delta.content
                if chunk.choices[0].finish_reason:
                    finish_reason = chunk.choices[0].finish_reason
            if chunk.usage:
                usage_data = chunk.usage

        return cls(
            content=accumulated_content,
            model_id=model_id,
            finish_reason=finish_reason,
            usage_prompt_tokens=usage_data.prompt_tokens if usage_data else None,
            usage_completion_tokens=usage_data.completion_tokens if usage_data else None,
            usage_total_tokens=usage_data.total_tokens if usage_data else None,
            response_id=last_chunk.id,
            created_timestamp=last_chunk.created,
            raw_response=chunks,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a dictionary."""
        return {
            "content": self.content,
            "model_id": self.model_id,
            "finish_reason": self.finish_reason,
            "usage_prompt_tokens": self.usage_prompt_tokens,
            "usage_completion_tokens": self.usage_completion_tokens,
            "usage_total_tokens": self.usage_total_tokens,
            "response_id": self.response_id,
            "created_timestamp": self.created_timestamp,
        }


@dataclass
class PlatformEmbeddingResponse:
    """Normalized response from a managed embedding platform."""

    embeddings: List[List[float]]
    model_id: str
    usage_prompt_tokens: Optional[int] = None
    usage_total_tokens: Optional[int] = None
    response_id: Optional[str] = None
    raw_response: Optional[Any] = None

    @classmethod
    def from_openai_embedding(cls, response: CreateEmbeddingResponse) -> "PlatformEmbeddingResponse":
        """Build a normalized response from an OpenAI CreateEmbeddingResponse."""
        embeddings = [data.embedding for data in response.data]
        usage = response.usage

        return cls(
            embeddings=embeddings,
            model_id=response.model,
            usage_prompt_tokens=usage.prompt_tokens if usage else None,
            usage_total_tokens=usage.total_tokens if usage else None,
            response_id=getattr(response, "id", None),
            raw_response=response,
        )


@dataclass
class PlatformMetadataEnvelope:
    """Envelope that carries platform metadata alongside model output."""

    response: PlatformModelResponse
    platform: str = "openai"
    api_version: Optional[str] = None
    request_id: Optional[str] = None
    system_fingerprint: Optional[str] = None
    organization: Optional[str] = None

    @classmethod
    def from_openai(cls, completion: ChatCompletion) -> "PlatformMetadataEnvelope":
        """Build metadata envelope from OpenAI ChatCompletion."""
        response = PlatformModelResponse.from_openai_completion(completion)
        return cls(
            response=response,
            platform="openai",
            request_id=completion.id,
            system_fingerprint=completion.system_fingerprint,
        )
