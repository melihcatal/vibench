"""Local request, response, and normalization helpers for Managed Model Platform Workflow.

Provider: Azure OpenAI Service (https://learn.microsoft.com/azure/ai-services/openai/)
SDK: openai >= 1.0.0 with AzureOpenAI client class.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class PlatformRequest:
    """Normalized request for Azure OpenAI chat completions."""
    deployment_id: str
    messages: list[dict[str, str]]
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stream: bool = False

    def to_api_kwargs(self) -> dict[str, Any]:
        """Convert to kwargs for the AzureOpenAI chat.completions.create call."""
        return {
            "model": self.deployment_id,
            "messages": self.messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "stream": self.stream,
        }


@dataclass
class PlatformUsage:
    """Token usage metadata from Azure OpenAI platform."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    @classmethod
    def from_azure_usage(cls, usage_obj: Any) -> PlatformUsage:
        """Parse usage from an Azure OpenAI response usage object."""
        return cls(
            prompt_tokens=getattr(usage_obj, "prompt_tokens", 0),
            completion_tokens=getattr(usage_obj, "completion_tokens", 0),
            total_tokens=getattr(usage_obj, "total_tokens", 0),
        )

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass
class PlatformResponse:
    """Normalized response from Azure OpenAI platform."""
    content: str = ""
    finish_reason: str = ""
    model_id: str = ""
    usage: PlatformUsage = field(default_factory=PlatformUsage)
    system_fingerprint: Optional[str] = None
    request_id: Optional[str] = None
    prompt_filter_results: Optional[list[dict]] = None
    content_filter_results: Optional[dict] = None

    @classmethod
    def from_azure_response(cls, response: Any) -> PlatformResponse:
        """Parse an Azure OpenAI chat completion response into normalized form.

        Args:
            response: OpenAI API response object (Azure-backed).
        """
        choice = response.choices[0] if response.choices else None
        message = choice.message if choice else None

        prompt_filter = None
        if hasattr(response, "prompt_filter_results") and response.prompt_filter_results:
            prompt_filter = response.prompt_filter_results

        content_filter = None
        if choice and hasattr(choice, "content_filter_results") and choice.content_filter_results:
            content_filter = choice.content_filter_results

        request_id = None
        if hasattr(response, "request_id"):
            request_id = response.request_id

        return cls(
            content=message.content if message and message.content else "",
            finish_reason=choice.finish_reason if choice else "",
            model_id=response.model or "",
            usage=PlatformUsage.from_azure_usage(response.usage) if response.usage else PlatformUsage(),
            system_fingerprint=getattr(response, "system_fingerprint", None),
            request_id=request_id,
            prompt_filter_results=prompt_filter,
            content_filter_results=content_filter,
        )

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["usage"] = self.usage.to_dict()
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class StreamingChunk:
    """Normalized chunk from a streamed Azure OpenAI response."""
    content: str = ""
    finish_reason: Optional[str] = None
    index: int = 0

    @classmethod
    def from_azure_chunk(cls, chunk: Any) -> StreamingChunk:
        """Parse a streaming chunk from Azure OpenAI."""
        choice = chunk.choices[0] if chunk.choices else None
        delta = choice.delta if choice else None

        return cls(
            content=delta.content if delta and delta.content else "",
            finish_reason=choice.finish_reason if choice else None,
            index=choice.index if choice else 0,
        )


@dataclass
class SafetyResult:
    """Result of Azure AI Content Safety check."""
    is_safe: bool = True
    categories: dict[str, str] = field(default_factory=dict)
    blocklists_matched: list[dict] = field(default_factory=list)
    raw_response: Optional[dict] = None

    @classmethod
    def from_azure_safety(cls, response: Any) -> SafetyResult:
        """Parse Azure AI Content Safety AnalyzeTextResponse."""
        categories = {}
        if hasattr(response, "categories_analysis") and response.categories_analysis:
            for cat in response.categories_analysis:
                cat_name = cat.category if hasattr(cat, "category") else str(cat)
                severity = cat.severity if hasattr(cat, "severity") else None
                categories[str(cat_name)] = str(severity)

        blocklists = []
        if hasattr(response, "blocklists_result") and response.blocklists_result:
            if hasattr(response.blocklists_result, "blocklists_match"):
                for m in response.blocklists_result.blocklists_match:
                    blocklists.append({
                        "blocklist_name": m.blocklist_name if hasattr(m, "blocklist_name") else "",
                        "match_details": [
                            {
                                "description": d.description if hasattr(d, "description") else "",
                                "snippet": d.snippet if hasattr(d, "snippet") else "",
                            }
                            for d in getattr(m, "matches", [])
                        ],
                    })

        is_safe = True
        if hasattr(response, "hate_result") and response.hate_result:
            if getattr(response.hate_result, "severity", 0) >= 4:
                is_safe = False
        if hasattr(response, "self_harm_result") and response.self_harm_result:
            if getattr(response.self_harm_result, "severity", 0) >= 4:
                is_safe = False
        if hasattr(response, "sexual_result") and response.sexual_result:
            if getattr(response.sexual_result, "severity", 0) >= 4:
                is_safe = False
        if hasattr(response, "violence_result") and response.violence_result:
            if getattr(response.violence_result, "severity", 0) >= 4:
                is_safe = False

        return cls(
            is_safe=is_safe,
            categories=categories,
            blocklists_matched=blocklists,
            raw_response=response.as_dict() if hasattr(response, "as_dict") else None,
        )


def normalize_messages(text: str, *, system_prompt: Optional[str] = None) -> list[dict[str, str]]:
    """Build a messages list for Azure OpenAI from raw text input.

    Args:
        text: The user query text.
        system_prompt: Optional system prompt.

    Returns:
        List of message dicts compatible with Azure OpenAI chat completions.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": text})
    return messages
