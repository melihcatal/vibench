"""Define local request, response, and normalization helpers for Managed Model Platform Workflow.

Uses Azure OpenAI Service conventions for request/response structures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ModelRequest:
    """Normalized request for Azure OpenAI model invocation."""

    prompt: str
    deployment: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 2048
    system_prompt: Optional[str] = None
    top_p: float = 1.0
    stream: bool = False

    def to_openai_messages(self) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass
class PlatformMetadata:
    """Provider platform metadata from Azure OpenAI responses."""

    model: str = ""
    usage_prompt_tokens: int = 0
    usage_completion_tokens: int = 0
    usage_total_tokens: int = 0
    resource_id: str = ""
    deployment_name: str = ""
    request_id: str = ""
    content_filter_result: dict[str, Any] = field(default_factory=dict)
    raw_response: Any = None


@dataclass
class ModelResponse:
    """Normalized response from Azure OpenAI model invocation."""

    text: str = ""
    finish_reason: str = ""
    metadata: Optional[PlatformMetadata] = None

    def extract_text(self) -> str:
        return self.text


def parse_azure_response(raw_response: Any) -> ModelResponse:
    """Parse an Azure OpenAI ChatCompletion response into a normalized ModelResponse."""
    from openai.types.chat import ChatCompletion

    if not isinstance(raw_response, ChatCompletion):
        raise TypeError(f"Expected ChatCompletion, got {type(raw_response)}")

    choice = raw_response.choices[0] if raw_response.choices else None
    text = ""
    finish_reason = ""
    if choice and choice.message:
        text = choice.message.content or ""
        finish_reason = choice.finish_reason or ""

    usage = raw_response.usage
    metadata = PlatformMetadata(
        model=raw_response.model,
        usage_prompt_tokens=usage.prompt_tokens if usage else 0,
        usage_completion_tokens=usage.completion_tokens if usage else 0,
        usage_total_tokens=usage.total_tokens if usage else 0,
        request_id=getattr(raw_response, "id", ""),
        raw_response=raw_response,
    )

    return ModelResponse(text=text, finish_reason=finish_reason, metadata=metadata)


def build_streaming_chunks(raw_stream: Any) -> list[str]:
    """Collect text chunks from an Azure OpenAI streaming response."""
    chunks: list[str] = []
    for chunk in raw_stream:
        delta = chunk.choices[0].delta if chunk.choices else None
        if delta and delta.content:
            chunks.append(delta.content)
    return chunks
