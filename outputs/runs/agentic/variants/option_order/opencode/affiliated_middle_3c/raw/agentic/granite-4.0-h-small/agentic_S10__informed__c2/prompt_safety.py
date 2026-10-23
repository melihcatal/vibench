# Prompt safety check using Alibaba Content Moderation SDK

import os
from alibabacloud_green20200501 import client as green_client
from alibabacloud_tea_openapi import models as open_api_models
from model_client import parse_chat_response

# -------------------------------------------------
# Alibaba Content Moderation client configuration
# -------------------------------------------------
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
REGION_ID = os.getenv("ALIBABA_CLOUD_REGION_ID", "cn-hangzhou")

config = open_api_models.Config(
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
    region_id=REGION_ID,
)
client = green_client.Client(config)


def is_prompt_safe(prompt_text: str) -> bool:
    """Check if a prompt is safe using Alibaba Content Moderation API."""
    response = client.detect_text_content(
        DetectTextContentRequest={
            "Content": prompt_text,
            "Scene": ["ads", "porn", "politics", "terrorism"],
        }
    )
    # Simplified check: assume safe if no violations returned
    return response.dict().get("Data", {}).get("Violations", []) == []


def sanitize_prompt(prompt_text: str) -> str:
    """Return a sanitized version or empty string if unsafe."""
    if not is_prompt_safe(prompt_text):
        return "<REDACTED - unsafe prompt>"
    return prompt_text


# Example usage (uncomment to test)
# safe = sanitize_prompt("Write a phishing email...")
# print(safe)
