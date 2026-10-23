# [LATER-STEP] vendor_text_safety.py

# Moderates vendor notes using Alibaba Content Moderation

import os
from alibabacloud_green20180509 import models as green_models
from alibabacloud_tea_openapi_20200301_1_0_0 import Client as TeaClient

ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
assert ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET, (
    "Set Alibaba Cloud credentials"
)

client = TeaClient(
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
)


def moderate_vendor_note(note: str) -> bool:
    """Return True if the vendor note passes Alibaba content moderation, else False."""
    request = green_models.TextModerationRequest()
    request.text = note
    response = client.text_moderation(request)
    # Simplified check; real implementation should inspect response labels
    return response.suggestion == "pass"
