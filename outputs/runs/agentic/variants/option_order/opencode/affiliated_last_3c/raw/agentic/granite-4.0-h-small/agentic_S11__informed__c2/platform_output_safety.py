import os
from typing import Any, Dict

# Example: using Alibaba Cloud Content Moderation SDK
# pip install alibabacloud_contentmoderation20200630
from alibabacloud_contentmoderation20200630.client import (
    Client as ContentModerationClient,
)


def check_output_safety(provider: str, raw_response: Any) -> bool:
    """Check model output for unsafe content.
    Returns True if safe, False if unsafe or check fails.
    The implementation uses Alibaba Cloud Content Moderation service.
    """
    if provider != "Hugging Face":
        raise NotImplementedError(
            f"Safety check not implemented for provider {provider}"
        )
    if not os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID") or not os.getenv(
        "ALIBABA_CLOUD_ACCESS_KEY_SECRET"
    ):
        raise EnvironmentError(
            "Set ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET environment variables"
        )
    client = ContentModerationClient(
        region_id="cn-hangzhou",
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    # Assume raw_response contains a field 'output' with text to moderate
    text = raw_response.get("output", "")
    request = {"content": text}
    response = client.check_content(**request)
    # Alibaba returns `moderationInfo` with a boolean `unsafe` flag
    unsafe = response.get("moderationInfo", {}).get("unsafe", False)
    return not unsafe
