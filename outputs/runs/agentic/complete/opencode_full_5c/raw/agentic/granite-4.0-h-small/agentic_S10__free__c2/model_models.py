# model_models.py
# [HELPER]
"""Local request, response, and normalization helpers for hosted LLM tasks.

This module defines lightweight dataclasses and utilities to shape
input prompts and normalize model outputs into predictable structures,
making the higher‑level integration files easier to read and maintain.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LLMRequest:
    """Normalization of request parameters for hosted LLM endpoints.

    Attributes:
        model: Identifier of the hosted model family.
        messages: Sequence of message role/content pairs.
        temperature: Sampling temperature.
        max_tokens: Optional maximum output length.
        stream: Whether to enable streaming (for chat_stream only).
    """

    model: str = "gpt-4o-mini"
    messages: List[Dict[str, Any]] = field(default_factory=list)
    temperature: float = 0.2
    max_tokens: Optional[int] = None
    stream: bool = False


@dataclass
class LLMRawResponse:
    """Raw shape of a raw HTTP response from the LLM provider.

    Attributes:
        raw_content: Raw server payload (usually JSON string).
        status_code: HTTP status returned.
        headers: Response headers.
    """

    raw_content: str
    status_code: int
    headers: Dict[str, str]


@dataclass
class LLMNormalizedResponse:
    """≈ Normalized outer shape of successful chat completions.

    Attributes:
        choices: List containing at least one `choice` object.
        usage: Usage statistics (optional, may be absent for streaming).
    """

    choices: List[Dict[str, Any]]
    usage: Optional[Dict[str, int]] = None
