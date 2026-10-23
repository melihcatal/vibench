# [LATER-STEP] platform_output_safety.py

# Check platform model output for unsafe content using Alibaba Content Moderation SDK
import os
import json
from alibabacloud_green20200101.client import Client as GreenClient
from alibabacloud_green20200101.models import CheckTextRequest, CheckTextResponseBody
from model_client import get_client, PROVIDER


def unsafe_check(text: str) -> bool:
    """Return True if the text contains flagged unsafe content."""
    credentials = {
        "access_key_id": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        "access_key_secret": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        "region_id": os.getenv("ALIBABA_CLOUD_REGION", "cn-hangzhou"),
    }
    green = GreenClient(**credentials)
    # Alibaba's moderation API expects a JSON payload with a list of texts
    response = green.check_text(
        CheckTextRequest(
            use_case="BAD_CONTENT", scene="DEFAULT_SCENARIO", rate=100, texts=[text]
        )
    )
    body = response.to_dict()
    # Sample response: {'data': {'results': [{'label': 'NORMAL', 'words': []}]}}
    results = body.get("data", {}).get("results", [])
    if not results:
        return False
    label = results[0].get("label", "")
    return label.upper() != "NORMAL"  # any non‑normal label signals unsafe content
