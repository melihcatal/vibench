# platform_output_safety.py
"""Check platform model output for unsafe content using Alibaba Content Moderation SDK.
This module receives the raw generated text and a ProviderInfo struct, sends the text to
the Alibaba Content Moderation service, and returns a safety verdict.
"""

import os
import json
from typing import Dict, Any
from alibabacloud_green20191226.client import Client as GreenClient
from alibabacloud_green20191226.models import DetectTextRequest
from model_models import ProviderInfo, ApiResponse


def verify_safety(text: str, provider_info: ProviderInfo) -> Dict[str, Any]:
    """Call Alibaba Content Moderation and return a safety report."""
    # Initialise client – expects env vars ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET
    green = GreenClient(endpoint="green.cn-hangzhou.aliyuncs.com",
                         access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                         access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"))
    request = DetectTextRequest(
        scene="text",
        content=text,
        restrict_info=True
    )
    response = green.detect_text(request)
    # Alibaba returns JSON with \"code\", \"message\", and \"data\" fields
    result = response.result()
    verdict = {
        "safe": result.get('safe', True),
        "categories": result.get('categories', []),
        "detail": result.get('detail', [])
    }
    return {
        "text": text,
        "metadata": provider_info.__dict__ if provider_info else {},
        "safety": verdict
    }

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Safety check for model output")
    parser.add_argument("text", help="Generated text to evaluate")
    args = parser.parse_args()
    print(json.dumps(verify_safety(args.text, ProviderInfo('','',{},{}) ), indent=2))
