import os
from typing import Dict, Any, Optional

from alibabacloud_green20220302.client import Client as GreenClient
from alibabacloud_green20220302.models import (
    TextModerationRequest,
    TextModerationResponse,
)
from alibabacloud_tea_util.models import RuntimeOptions


def check_prompt_safety(
    text: str,
    block_threshold: float = 0.8,
) -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using Alibaba Content Moderation.
    """
    access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

    if not access_key_id or not access_key_secret:
        raise ValueError("Alibaba Cloud credentials not set in environment variables")

    client = GreenClient(
        config={
            "access_key_id": access_key_id,
            "access_key_secret": access_key_secret,
            "region_id": "cn-shanghai",
        }
    )

    request = TextModerationRequest(
        service_parameters=text,
    )

    runtime = RuntimeOptions()
    response: TextModerationResponse = client.text_moderation_with_options(
        request, runtime
    )

    if response.status_code != 200:
        raise RuntimeError(f"Content moderation failed: {response.status_message}")

    result = response.body.result
    is_blocked = result.suggestion == "block" and result.confidence >= block_threshold

    return {
        "safe": not is_blocked,
        "confidence": result.confidence,
        "suggestion": result.suggestion,
        "labels": [label.label for label in result.labels] if result.labels else [],
    }
