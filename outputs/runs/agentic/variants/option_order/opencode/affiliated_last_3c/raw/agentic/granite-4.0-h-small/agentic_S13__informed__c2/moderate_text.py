# moderate_text.py
# SAME-SCENARIO implementation
# Alibaba Content Moderation (alibabacloud_green SDK) for scoring unsafe content

import os

from alibabacloud_green import AcsClient
from alibabacloud_green.request import ContentModerationRequest

client = AcsClient(
    access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
)


def moderate_single(user_text: str, category: str = "abuse") -> dict:
    """Request moderation and return the raw provider response."""
    request = ContentModerationRequest(content=user_text, category=category)
    response = client.do_action_with_exception(request)
    return response
