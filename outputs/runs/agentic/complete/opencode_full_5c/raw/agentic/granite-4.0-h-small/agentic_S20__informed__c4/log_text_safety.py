import os
import requests
from observability_models import LogEvent


def log_text_safety(log_event: LogEvent) -> bool:
    """Check selected log message text for unsafe content using Tisane Text Moderation API.

    Returns True if the message is considered safe, False otherwise.
    """
    api_key = os.getenv("TISANE_API_KEY")
    if not api_key:
        raise RuntimeError("TISANE_API_KEY environment variable not set")

    url = "https://api.tisane.ai/v1/moderate"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"text": log_event.message, "language": "en"}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        resp.raise_for_status()
        result = resp.json()
        # Assume Tisane returns {'flags': []} for safe, otherwise flagged items
        return not result.get("flags")
    except Exception as e:
        print(f"Safety check failed: {e}")
        # In case of failure, treat as unsafe to avoid false positives
        return False
