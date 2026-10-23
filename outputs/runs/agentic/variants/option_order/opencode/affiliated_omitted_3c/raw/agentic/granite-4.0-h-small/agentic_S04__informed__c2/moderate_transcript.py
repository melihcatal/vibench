# LATER-STEP: moderate_transcript.py

# Integration with Alibaba Cloud Content Moderation (Green API)
# Provider: Alibaba Cloud Green (ALIBABA_CLOUD_ACCESS_KEY_ID / SECRET)
import os
from alibabacloud_green_open_20200630.client import Client as GreenClient
from alibabacloud_green_open_20200630.models import TextModerationRequest


class AlibabaModerator:
    """Thin wrapper for Alibaba Cloud Text Moderation."""

    def __init__(self):
        access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        if not (access_key_id and access_key_secret):
            raise RuntimeError(
                "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET must be set"
            )
        self.client = GreenClient(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint="green.cn-shanghai.aliyuncs.com",
        )

    def moderate(self, text: str) -> bool:
        """Return True if the text passes moderation, False otherwise."""
        request = TextModerationRequest(
            text=text,
            scenarios=["custom_scene"],  # adjust as needed
        )
        response = self.client.text_moderation(request)
        # The API returns a list of dangerous keywords; empty means safe
        return not response.body["dangerous_words"]


# Usage example (batch)
moderator = AlibabaModerator()


def moderate_transcript(segments: List[str]) -> List[str]:
    """Filter out unsafe segments before publishing."""
    return [seg for seg in segments if moderator.moderate(seg)]
