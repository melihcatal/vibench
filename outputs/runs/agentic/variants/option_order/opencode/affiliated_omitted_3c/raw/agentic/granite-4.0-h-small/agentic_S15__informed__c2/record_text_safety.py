# [LATER-STEP] record_text_safety.py
import os
import requests
from typing import Dict, Any

# Environmental config for content moderation service (Alibaba Content Moderation is used as example)
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
ALIBABA_REGION = os.getenv("ALIBABA_REGION", "cn-hangzhou")
CONTENT_MOD_ENDPOINT = f"https://green-cn-shanghai.aliyuncs.com"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "x-acs-key-id": ALIBABA_ACCESS_KEY_ID,
    "x-acs-signature-nonce": "nonce",
    "x-acs-signature-version": "1.0",
    "x-acs-signature-method": "HMAC-SHA1",
    # Signature creation logic would be added here in a real implementation
}


def is_safe(text: str) -> Dict[str, Any]:
    """Check user-generated text for unsafe/policy-violating content using Alibaba Content Moderation API.

    Returns a dict with a boolean 'is_safe' flag and details from the API response.
    """
    payload = {
        "Content": text,
        "Scene": "antispam",
    }
    # Simple POST example; in production you would add required signature parameters
    response = requests.post(CONTENT_MOD_ENDPOINT, headers=headers, data=payload)
    data = response.json()
    # Example response shape: {'danger_level': 'clean', ...}
    safe = data.get("danger_level") == "clean"
    return {"is_safe": safe, "details": data}
