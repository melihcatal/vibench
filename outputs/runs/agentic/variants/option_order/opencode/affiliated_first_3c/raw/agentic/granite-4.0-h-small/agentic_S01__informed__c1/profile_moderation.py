import os
import requests
from alibabacloud_green20191223.client import AcsClient
from alibabacloud_green20191223.models import TextModerationRequest


def moderate_profile_text(text: str) -> bool:
    """Moderate profile text for safety before account activation using Alibaba Content Moderation."""
    client = AcsClient(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    request = TextModerationRequest()
    request.Text = text
    response = client.text_moderation(request)
    return response.body.data[0].suggestion == "pass"
