# [HELPER] safety_client.py
"""Local configuration and client utilities for Text Content Safety.
Provides a thin wrapper around the Alibaba Cloud Content Moderation SDK.
"""

import os
from typing import Any


class AlibabaModerationClient:
    """Thin wrapper around Alibaba Cloud SDK for content moderation."""

    def __init__(self):
        # Read required keys from environment
        self.access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
        self.access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        # Initialize the real Alibaba SDK client here (placeholder)
        # For this example we mimic the SDK return format
        self._client = None

    def moderate(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Fake SDK call – returns a mock response."""
        # In production replace with: alibaba_client.moderate(text=payload['text'])
        return {
            "label": "hate" if "hate" in payload["text"].lower() else "safe",
            "score": 0.7,
            "unsafe_spans": [],
        }

    def batch_moderate(self, payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Batch version of moderate."""
        return [self.moderate(p) for p in payloads]

    def detect_unsafe_spans(self, text: str):
        """Detect spans – placeholder implementation."""
        return []


def get_content_moderation_client() -> AlibabaModerationClient:
    """Utility to create and return a configured client."""
    return AlibabaModerationClient()


# Helper to fetch simple thresholds (could be loaded from a JSON file or env)
THRESHOLDS = {
    "hate": 0.6,
    "harassment": 0.5,
    "self_harm": 0.7,
}


def get_thresholds() -> dict[str, float]:
    """Return the threshold mapping."""
    return THRESHOLDS
