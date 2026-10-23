"""Provide local configuration and client helper utilities for Text Content Safety.

Uses OpenAI as the concrete provider (api.openai.com, text-moderation-latest model).
"""

import os
from typing import Any, Dict

from openai import OpenAI


_SAFETY_CONFIG_CACHE: Dict[str, Any] = {}


def get_safety_config() -> Dict[str, Any]:
    """Load safety configuration from environment or config file.

    Reads OpenAI-specific configuration including OPENAI_API_KEY and
    optional safety thresholds from environment variables.

    Returns:
        Dict with provider configuration for OpenAI moderation.
    """
    if _SAFETY_CONFIG_CACHE:
        return dict(_SAFETY_CONFIG_CACHE)

    config: Dict[str, Any] = {
        "provider": "openai",
        "provider_endpoint": "api.openai.com",
        "moderation_model": "text-moderation-latest",
        "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
        "max_batch_size": int(os.environ.get("SAFETY_MAX_BATCH_SIZE", "100")),
        "default_thresholds": {
            "hate": float(os.environ.get("SAFETY_THRESHOLD_HATE", "0.5")),
            "self-harm": float(os.environ.get("SAFETY_THRESHOLD_SELF_HARM", "0.5")),
            "sexual": float(os.environ.get("SAFETY_THRESHOLD_SEXUAL", "0.5")),
            "violence": float(os.environ.get("SAFETY_THRESHOLD_VIOLENCE", "0.5")),
        },
    }

    _SAFETY_CONFIG_CACHE.update(config)
    return dict(_SAFETY_CONFIG_CACHE)


def create_openai_client() -> OpenAI:
    """Create an authenticated OpenAI client for moderation calls.

    Uses OPENAI_API_KEY from environment or safety config.

    Returns:
        Configured OpenAI client instance targeting api.openai.com.
    """
    config = get_safety_config()
    api_key = config.get("openai_api_key", "")
    return OpenAI(api_key=api_key)


def build_moderation_payload(
    texts: list,
    model: str = "text-moderation-latest",
) -> Dict[str, Any]:
    """Build a moderation request payload for the OpenAI Moderation API.

    Args:
        texts: Single string or list of strings to moderate.
        model: OpenAI moderation model identifier (default: text-moderation-latest).

    Returns:
        Dict payload suitable for OpenAI's moderations.create method.
    """
    return {
        "model": model,
        "input": texts,
    }
