# redact_unsafe.py
# SAME-SCENARIO implementation
# Uses Alibaba Content Moderation to find unsafe spans and redacts them

import os

from alibabacloud_green import AcsClient
from alibabacloud_green.request import ContentModerationRequest

client = AcsClient(
    access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
)


def redact_unsafe(text: str) -> str:
    """Redact unsafe spans detected by Alibaba Content Moderation.

    Returns a sanitized version of the input text with unsafe portions replaced by '[REDACTED]'.
    """
    # First get the moderation result to locate unsafe spans
    moderation = client.content_moderation_with_exception(
        ContentModerationRequest(content=text, category="abuse")
    )
    # Assume moderation result contains a 'data.locations' list similar to Alibaba's format
    # This is illustrative; adjust to actual response structure
    redacted = text
    if "data" in moderation and "locations" in moderation["data"]:
        for loc in moderation["data"]["locations"]:
            start, end = loc["start"], loc["end"]
            redacted = redacted[:start] + "[REDACTED]" + redacted[end:]
    return redacted
