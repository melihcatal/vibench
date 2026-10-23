# record_text_safety.py
"""
Later-step implementation file.

Checks user-generated text fields in documents for unsafe / prohibited content using Alibaba Content Moderation API.
"""

import os
import json
from typing import List, Dict
from alibabacloud_tea_openapi_20210524.client import Client as TeaOpenapiClient
from alibabacloud_tea_openapi_20210524.models import Config as TeaConfig
from alibabacloud_green_20210601.client import Client as TeaGreenClient
from alibabacloud_green_20210601.models import (
    TextModerationRequest as TeaTextModerationRequest,
)

# Provider credentials
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_ACCESS_KEY_SECRET")
if not ALIBABA_ACCESS_KEY_ID or not ALIBABA_ACCESS_KEY_SECRET:
    raise RuntimeError(
        "ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET must be set"
    )

# Alibaba Cloud config
config = TeaConfig(
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
    region_id="cn-hangzhou",
    # Endpoint for Content Moderation service
    endpoint="green.cn-hangzhou.aliyuncs.com",
)
client = TeaGreenClient(config)


def is_content_safe(documents: List[dict], field_path: str) -> List[Dict[str, bool]]:
    """
    Scan a list of documents for unsafe text in the given JSON field path.

    Args:
        documents (List[dict]): List of JSON documents.
        field_path (str): Dot‑separated path, e.g., \"metadata.comments\".

    Returns:
        List[Dict[str, bool]]: One result per document, with \"safe\" (bool) and \"detail\" (dict).
    """
    results = []
    for doc in documents:
        # Traverse JSON using dot notation
        value = doc
        for part in field_path.split("."):
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                # Field missing => consider safe
                results.append({"safe": True, "detail": {}})
                break
        else:
            # Only run moderation if field exists
            text = str(value)
            request = TeaTextModerationRequest()
            request.scene = "politics"
            request.text = text
            response = client.text_moderation(request)
            # Simplify response to safe flag + details
            safe = response.data and response.data.suggestion == "PASS"
            results.append({"safe": safe, "detail": response.data})
    return results
