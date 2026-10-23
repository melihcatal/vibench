import os
import openid_client
import requests

# Alibaba Content Moderation SDK configuration
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
ENDPOINT = "https://green.cn-shanghai.aliyuncs.com"

moderator = openid_client.AccessTokenClient(
    grant_type="client_credentials",
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
    endpoint=ENDPOINT,
)


def moderate_profile_text(profile_text: str) -> dict:
    """Moderate profile text with Alibaba Cloud Content Moderation.

    Returns a dict with 'pass' boolean and any flagged categories.
    """
    response = moderator.core.do_action_with_exception(
        "ContentModeration",
        {
            "Action": "ContentModeration",
            "Version": "2020-11-01",
            "RegionId": "cn-shanghai",
            "Content": profile_text,
            "Scene": "image",  # placeholder; moderation for text also available
        },
    )
    # Simple mapping to boolean
    return {
        "pass": response.get("SafeResult", 1) == 1,
        "details": response.get("Data", []),
    }
