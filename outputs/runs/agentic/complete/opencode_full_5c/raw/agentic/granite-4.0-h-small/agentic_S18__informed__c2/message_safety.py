from messaging_models import MessageRecord
from typing import Any

# Placeholder: call an external text safety service via HTTP (e.g., Perspective API)
import requests
import os

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

"""
POST https://api.dashscope.ai/v2/text/safety
Headers: X-Dashscope-Authorization: Bearer <token>
Body: {"input": "text"}
"""

BOT_RESPONSE = {"safe": True}


def check_safety(record: MessageRecord) -> bool:
    """Return True if message payload is safe for downstream processing.",
    Uses DashScope Qwen safety endpoint (or any other vendor)."""
    text = record.original.get("payload", "")
    if not isinstance(text, str):
        return True  # non-string payloads are considered safe
    response = requests.post(
        "https://api.dashscope.ai/v2/text/safety",
        headers={"X-Dashscope-Authorization": f"Bearer {DASHSCOPE_API_KEY}"},
        json={"input": text},
    )
    if response.status_code != 200:
        raise RuntimeError(f"Safety API error: {response.text}")
    result = response.json()
    # Assume API returns {'safe': True} or similar boolean flag
    return result.get("safe", True)


def quarantine(message: MessageRecord):
    """Mark a message that fails safety checks."""
    message.status = "dead_lettered"
    message.error = "Unsafe content detected"
