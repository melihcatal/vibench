# visual_safety_text.py
"""Check generated visual labels for unsafe or policy‑sensitive text.

Uses Alibaba Content Moderation SDK as the concrete provider to scan any
extracted text from images for profanity, hate speech, or other violations."

import json
import os
from alibabacloud_green20191227.client import AcsClient, Config
from alibabacloud_green20191227.models import TextScanRequest
from dotenv import load_dotenv

load_dotenv()

ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

# Initialize Alibaba Content Moderation client – the SDK handles credential loading
config = Config()
config.access_key_id = ALIBABA_ACCESS_KEY_ID
config.access_key_secret = ALIBABA_ACCESS_KEY_SECRET
config.region_id = "cn-hangzhou"  # adjust as needed
client = AcsClient(config)

def scan_text_for_unsafe(text: str) -> dict:
    """Send a list of strings to Alibaba Content Moderation and return the safe flag."""
    request = TextScanRequest()
    request.set_Text(text)
    response = client.text_scan(request)
    # Example response format (simplified):
    # {"data": {"textScanResult": {"safe": true, "detail": {}}}}
    try:
        data = json.loads(response.http_response.body.read().decode())
        safe = data["data"]["textScanResult"].get("safe", True)
        details = data["data"]["textScanResult"].get("detail", [])
        return {
            "safe": safe,
            "details": details
        }
    except Exception as e:
        # In production, log and fallback to safe=False
        return {
            "safe": False,
            "details": ["Error processing text: " + str(e)]
        }
