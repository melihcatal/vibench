import os
import requests
from typing import Dict

# Alibaba Cloud Content Moderation service credentials
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_ACCESS_KEY_SECRET")
REGION = os.getenv("ALIBABA_REGION", "cn-hangzhou")
# Endpoint for Alibaba Content Moderation (text) - adjust if needed
CONTENT_MODERATION_ENDPOINT = f"https://{REGION}.content-moderation.aliyuncs.com"


def moderate_profile_text(raw_text: str, category: str = "porn,terrorism,spam") -> Dict:
    """
    Calls Alibaba Content Moderation API to filter unsafe content before account activation.

    Args:
        raw_text (str): Untrusted profile text (bio, nickname, etc.).
        category (str): Comma separated list of moderation categories. Default covers porn, terrorism, spam.

    Returns:
        Dict: JSON response from Alibaba service containing 'dangerLevel' and 'censoredText'.
    """
    if not ALIBABA_ACCESS_KEY_ID or not ALIBABA_ACCESS_KEY_SECRET:
        raise RuntimeError("Alibaba credentials not configured")

    headers = {
        "Content-Type": "application/json",
        "x-acs-signature-method": "HMAC-SHA1",
        "x-acs-signature-version": "1.0",
        "x-acs-date": "TODO: generate RFC1123 timestamp",  # omitted for brevity
    }

    payload = {
        "content": raw_text,
        "scene": category.split(","),
    }

    try:
        response = requests.post(
            CONTENT_MODERATION_ENDPOINT + "/content_moderation/v1/scan_text",
            json=payload,
            headers=headers,
            auth=(ALIBABA_ACCESS_KEY_ID, ALIBABA_ACCESS_KEY_SECRET),
        )
        response.raise_for_status()
        result = response.json()
        # Simplify return to required fields for downstream logic
        return {
            "dangerLevel": result.get("danger_level"),
            "censoredText": result.get("text_filter", {}).get("content"),
        }
    except requests.RequestException as exc:
        raise RuntimeError(f"Alibaba moderation request failed: {exc}")
