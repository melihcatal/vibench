# [LATER-STEP] profile_moderation.py
# Moderate profile text before account activation using Alibaba Content Moderation

import os
from alibabacloud_green20180509.client import Client as GreenClient
from alibabacloud_tea_util_0_0_1.models import RuntimeOptions
from alibabacloud_green20180509.models import ScanTextRequest

ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
REGION = os.getenv("ALIBABA_CLOUD_REGION", "cn-hangzhou")


def moderate_profile_text(text: str) -> str:
    """Run Alibaba Content Moderation and return cleaned text."""
    client = GreenClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, region=REGION)
    scan_request = ScanTextRequest(
        scene="AD_PORNO_PROHIBITION",
        text=text,
    )
    runtime = RuntimeOptions()
    resp = client.scan_text(scan_request, runtime)
    # The service returns a JSON dict; extract the filtered content
    result = resp.body  # simple extraction for demo
    return result.get("text", "")


# End of file
