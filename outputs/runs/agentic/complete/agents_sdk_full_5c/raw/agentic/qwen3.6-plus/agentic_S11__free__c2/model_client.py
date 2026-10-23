"""Local configuration and client helper utilities for Managed Model Platform Workflow.

This module wraps OpenAI SDK client creation, API key resolution,
and default model configuration targeting the OpenAI platform
(api.openai.com).
"""

import os
from typing import Any

from openai import OpenAI

# ---------------------------------------------------------------------------
# OpenAI platform defaults
# ---------------------------------------------------------------------------

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL_DEFAULT = "https://api.openai.com/v1"

# Default OpenAI model identifier used across the workflow
PLATFORM_MODEL_DEFAULT = os.environ.get("OPENAI_MODEL_ID", "gpt-4o")


def _resolve_openai_api_key() -> str:
    """Return the OpenAI API key from the environment."""
    key = os.environ.get(OPENAI_API_KEY_ENV)
    if not key:
        raise RuntimeError(
            f"{OPENAI_API_KEY_ENV} environment variable is not set. "
            "An OpenAI API key is required to call api.openai.com."
        )
    return key


def get_openai_client(
    *,
    api_key: str | None = None,
    base_url: str = OPENAI_BASE_URL_DEFAULT,
    extra_kwargs: dict[str, Any] | None = None,
) -> OpenAI:
    """Create and return a configured OpenAI SDK client.

    The client targets the OpenAI platform at api.openai.com and uses
    the OPENAI_API_KEY environment variable by default.
    """
    resolved_key = api_key or _resolve_openai_api_key()
    kwargs: dict[str, Any] = {
        "api_key": resolved_key,
        "base_url": base_url,
    }
    if extra_kwargs:
        kwargs.update(extra_kwargs)
    return OpenAI(**kwargs)


def get_default_model_id() -> str:
    """Return the default OpenAI model identifier (gpt-4o by default)."""
    return PLATFORM_MODEL_DEFAULT


def build_messages(
    prompt: str,
    system_prompt: str | None = None,
    history: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    """Build an OpenAI chat messages list from components."""
    messages: list[dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})
    return messages


def safe_get_text(raw_response: Any) -> str:
    """Safely extract text content from a raw OpenAI ChatCompletion response."""
    if raw_response is None:
        return ""
    try:
        choices = getattr(raw_response, "choices", None)
        if choices:
            message = choices[0].message
            return getattr(message, "content", "") or ""
    except Exception:
        pass
    return ""
