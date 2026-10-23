"""Local request, response, and normalization helpers for Managed Model Platform Workflow.

Dataclasses and helpers for OpenAI platform interactions used across
the same-scenario and later-step integration files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any


# ---------------------------------------------------------------------------
# Request
# ---------------------------------------------------------------------------


@dataclass
class PlatformRequest:
    """Normalized request payload for an OpenAI chat completion call."""

    prompt: str
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 1024
    system_prompt: str | None = None
    history: list[dict[str, str]] | None = None

    def to_messages(self) -> list[dict[str, str]]:
        """Build the OpenAI messages list from request fields."""
        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        if self.history:
            messages.extend(self.history)
        messages.append({"role": "user", "content": self.prompt})
        return messages

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Response
# ---------------------------------------------------------------------------


@dataclass
class PlatformResponse:
    """Normalized response wrapping an OpenAI chat completion result."""

    text: str
    finish_reason: str | None = None
    model: str = "gpt-4o"
    raw_response: Any = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "finish_reason": self.finish_reason,
            "model": self.model,
        }


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------


@dataclass
class PlatformMetadata:
    """OpenAI platform metadata extracted from a ChatCompletion response."""

    model_id: str = "gpt-4o"
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    system_fingerprint: str | None = None
    response_id: str | None = None
    created: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Resource
# ---------------------------------------------------------------------------


@dataclass
class PlatformResource:
    """Represents an OpenAI model or deployment resource."""

    resource_id: str
    resource_type: str
    created: int
    owned_by: str


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------


def normalize_platform_text(text: str) -> str:
    """Clean and normalize text returned from an OpenAI model."""
    return text.strip()


def parse_json_output(text: str) -> Any:
    """Attempt to parse JSON embedded in OpenAI model output."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        lines = lines[1:] if lines else lines
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return json.loads(cleaned)
