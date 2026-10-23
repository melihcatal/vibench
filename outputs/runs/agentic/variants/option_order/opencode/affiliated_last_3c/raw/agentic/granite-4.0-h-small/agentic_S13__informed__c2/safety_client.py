# safety_client.py
# HELPER implementation
# Central configuration and client utilities for Text Content Safety

import os
from typing import Any, Dict

# Choose concrete provider: Alibaba Content Moderation (alibabacloud_green SDK)
from alibabacloud_green import AcsClient
from alibabacloud_green.request import ContentModerationRequest

# Global client instance (singleton)
_client: Any = None


def _init_client() -> None:
    global _client
    if _client is None:
        _client = AcsClient(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        )


def get_client() -> Any:
    """Return a configured Alibaba Cloud Content Moderation client."""
    if _client is None:
        _init_client()
    return _client


def call_moderation(text: str, category: str = "abuse") -> Dict[str, Any]:
    """Wrapper around Alibaba moderation API; returns raw response."""
    client = get_client()
    request = ContentModerationRequest(content=text, category=category)
    return client.content_moderation_with_exception(request)
