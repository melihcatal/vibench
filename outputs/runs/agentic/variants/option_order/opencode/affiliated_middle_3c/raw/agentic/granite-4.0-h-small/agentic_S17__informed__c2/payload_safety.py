# [LATER-STEP] payload_safety.py
# Check decrypted text payloads for unsafe content using Alibaba Content Moderation

from alibabacloud_green20200501.client import Client as GreenClient
from alibabacloud_tea_openapi.models import Config
import json


class PayloadSafetyChecker:
    """Utility to scan decrypted text with Alibaba Cloud Content Moderation API."""

    def __init__(self):
        # Minimal configuration – expects environment variables for auth
        config = Config(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            endpoint="green.cn-shanghai.aliyuncs.com",
        )
        self._client = GreenClient(config)

    def scan_text(self, text: str) -> dict:
        """Calls Alibaba Content Moderation API to detect unsafe content.

        Returns a dict containing the API raw response; frontend can decide if unsafe.
        """
        request = {
            "scene": "antispam",  # focus on unsafe / spam detection
            "content": text.encode("utf-8"),  # API expects bytes
        }
        response = self._client.text_antispam(request)
        # Return a simple boolean flag plus details for audit
        return {
            "safe": response.get("code") == "200",
            "details": response.get("data", {}),
        }


# Example usage (remove in production)
if __name__ == "__main__":
    checker = PayloadSafetyChecker()
    result = checker.scan_text(
        "This is a test message with unsafe link http://example.com"
    )
    print(result)
