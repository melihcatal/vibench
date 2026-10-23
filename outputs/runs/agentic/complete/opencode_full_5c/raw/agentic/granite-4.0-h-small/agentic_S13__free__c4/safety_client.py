# HELPER: safety_client.py
"""Local helper utilities for configuring and accessing the text‑content‑safety provider."""

import os
from typing import Any, Dict, Optional

# Concrete provider selection (placeholder for production API key / endpoint)
PROVIDER = os.getenv("TEXT_SAFETY_PROVIDER", "openai")
API_KEY = os.getenv("TEXT_SAFETY_API_KEY")


def get_moderation_client() -> Any:
    """Return a ready‑to‑use moderation client for the selected provider.

    Raises:
        RuntimeError if API key is missing or provider is unsupported.
    """
    if not API_KEY:
        raise RuntimeError("TEXT_SAFETY_API_KEY environment variable must be set")
    if PROVIDER == "openai":
        # Example using the OpenAI Python SDK (replace with actual import if needed)
        import openai

        openai.api_key = API_KEY
        return openai
    elif PROVIDER == "custom":
        # Example stub for a custom HTTP client – actual implementation omitted
        raise NotImplementedError("Custom provider not implemented")
    else:
        raise RuntimeError(f"Unsupported provider: {PROVIDER}")


# ---------------------------------------------------------------------------
# Utility to load optional configuration from a JSON/YAML file
# ---------------------------------------------------------------------------
import json

CONFIG_PATH = os.getenv("TEXT_SAFETY_CONFIG", "config/safety_config.json")


def load_config(path: str = CONFIG_PATH) -> Optional[Dict[str, Any]]:
    """Read optional safety configuration (e.g., category thresholds).

    Returns:
        Parsed dict or None if file not found.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
