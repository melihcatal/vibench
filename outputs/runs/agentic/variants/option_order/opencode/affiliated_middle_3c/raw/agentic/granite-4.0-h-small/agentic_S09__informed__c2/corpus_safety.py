# corpus_safety.py - LATER-STEP
# Check corpus text for policy violations before embedding

import os
import json
from typing import List

# Example provider: Alibaba Cloud Content Moderation SDK
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
if not (ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET):
    raise ValueError(
        "Set ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET"
    )

# Install via pip install alibabacloud_green alibabacloud_darab-invoke
from alibabacloud_green20191210 import client as green_client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_green20191210.models import TextRiskRequest

_client = None


def _get_green_client() -> green_client.GreenClient:
    """Lazy initialize Alibaba Content Moderation client."""
    global _client
    if _client is None:
        _client = green_client.GreenClient(
            endpoint="green.cn-shanghai.aliyuncs.com",
            access_key_id=ALIBABA_ACCESS_KEY_ID,
            access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
            security_token=None,
        )
    return _client


def check_corpus(texts: List[str]) -> List[dict]:
    """
    Run Alibaba Content Moderation checks on a list of corpus strings.

    Returns a list of dictionaries with fields: 'status', 'suggestions', 'labels'.
    """
    client = _get_green_client()
    request = TextRiskRequest(
        texts=list(texts),
        # optional: scene='ad' or 'terrorism' etc.
        scene="ad",
    )
    raw = client.text_risk(request)
    # The SDK returns a parsed model; convert to simple dict for downstream use
    return json.loads(
        raw.request_id
    )  # placeholder; actual response parsing depends on SDK
