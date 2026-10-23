import os
from alibabacloud_green20221115 import models as green_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_green20221115.client import Client as GreenClient

# Alibaba Cloud Content Moderation configuration from environment variables
ALIBABA_CLOUD_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
REGION_ID = "cn-shanghai"  # Example region, adjust as needed

# Build a Green client for text moderation
config = open_api_models.Config(
    access_key_id=ALIBABA_CLOUD_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_CLOUD_ACCESS_KEY_SECRET,
    region_id=REGION_ID,
)
client = GreenClient(config)


def moderate_profile_text(profile_text: str) -> dict:
    """Moderates profile text before account activation.

    Uses Alibaba Cloud Content Moderation API to detect profanity
    and other policy violations. Returns a dict with a 'clean' flag
    and any flagged categories.
    """
    request = green_models.TextModerationRequest(
        comment=profile_text,
        scene="porn",  # Extend with other scenes like 'politics', 'terrorism' if needed
    )
    response = client.text_moderation(request)
    # Normalize response to a simple dict
    return {
        "clean": response.dict()["suggestion"] == "pass",
        "categories": response.dict()["categories"],
    }
