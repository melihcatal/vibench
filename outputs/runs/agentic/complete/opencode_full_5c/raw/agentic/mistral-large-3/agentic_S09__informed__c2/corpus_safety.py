import os
from typing import List, Dict, Any


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """
    Check corpus text for harmful content using Alibaba Content Moderation.
    Requires ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET environment variables.
    """
    from alibabacloud_green20220302.client import Client as GreenClient
    from alibabacloud_green20220302.models import (
        TextModerationRequest,
        TextModerationResponse,
    )
    from alibabacloud_tea_util.models import RuntimeOptions
    from alibabacloud_tea_util.client import Client as UtilClient

    access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

    if not access_key_id or not access_key_secret:
        raise ValueError("Alibaba Cloud credentials not set in environment variables")

    config = {
        "access_key_id": access_key_id,
        "access_key_secret": access_key_secret,
        "region_id": "cn-shanghai",
    }
    client = GreenClient(config)
    runtime = RuntimeOptions()

    results = []
    for text in texts:
        request = TextModerationRequest(service_parameters=text)
        try:
            response = client.text_moderation_with_options(request, runtime)
            if UtilClient.is_unsuccessful(response):
                raise Exception(
                    f"Alibaba Content Moderation API error: {response.status_message}"
                )
            results.append(
                {
                    "text": text,
                    "safe": response.body.result.suggestion == "pass",
                    "labels": response.body.result.labels
                    if response.body.result.labels
                    else [],
                }
            )
        except Exception as e:
            results.append({"text": text, "safe": False, "error": str(e)})

    safe_count = sum(1 for r in results if r.get("safe", False))
    return {
        "total_texts": len(texts),
        "safe_texts": safe_count,
        "unsafe_texts": len(texts) - safe_count,
        "results": results,
    }
