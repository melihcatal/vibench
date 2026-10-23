"""Provide local configuration and client helper utilities for Managed Model Platform Workflow.

This module wraps the OpenAI Python SDK client with configuration loading,
retry handling, and provider-specific initialization helpers.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from openai import OpenAI, AsyncOpenAI, APIConnectionError, RateLimitError
from openai._exceptions import APIError


OPENAI_DEFAULT_MODEL = "gpt-4o"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_TTS_MODEL = "tts-1"
OPENAI_WHISPER_MODEL = "whisper-1"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def load_openai_config() -> Dict[str, str]:
    """Load OpenAI client configuration from environment variables.

    Reads OPENAI_API_KEY, OPENAI_BASE_URL (optional), and OPENAI_ORG_ID
    from the process environment.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI platform access."
        )

    config: Dict[str, str] = {"api_key": api_key}

    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        config["base_url"] = base_url

    org_id = os.environ.get("OPENAI_ORG_ID")
    if org_id:
        config["organization"] = org_id

    return config


def create_openai_client(**overrides: Any) -> OpenAI:
    """Create a synchronous OpenAI client with loaded configuration.

    Args:
        **overrides: Keyword arguments to override environment-sourced config.

    Returns:
        An openai.OpenAI instance ready for managed-model calls.
    """
    config = load_openai_config()
    config.update(overrides)
    return OpenAI(**config)


def create_openai_async_client(**overrides: Any) -> AsyncOpenAI:
    """Create an asynchronous OpenAI client with loaded configuration.

    Args:
        **overrides: Keyword arguments to override environment-sourced config.

    Returns:
        An openai.AsyncOpenAI instance ready for managed-model calls.
    """
    config = load_openai_config()
    config.update(overrides)
    return AsyncOpenAI(**config)


def resolve_deployment_model(model_id: Optional[str] = None) -> str:
    """Resolve the concrete OpenAI model identifier.

    Precedence:
      1. Explicit model_id argument
      2. OPENAI_MODEL environment variable
      3. OPENAI_DEFAULT_MODEL fallback
    """
    if model_id:
        return model_id
    env_model = os.environ.get("OPENAI_MODEL")
    if env_model:
        return env_model
    return OPENAI_DEFAULT_MODEL


def with_retry(func, max_retries: int = 3, backoff_base: float = 1.0):
    """Wrap a provider call with exponential-backoff retry on transient errors.

    Retries on openai.RateLimitError and openai.APIConnectionError only.
    """
    import time

    last_exc: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            return func()
        except (RateLimitError, APIConnectionError) as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                time.sleep(backoff_base * (2 ** attempt))
                continue
            raise
    raise last_exc  # type: ignore[misc]
