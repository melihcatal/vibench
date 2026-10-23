from typing import Dict, Any
import requests

"""Message safety check using watsonx guardrails (IBM service)."""

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

CONTENT_SAFETY_ENDPOINT = (
    "https://api.us-south.watson.ibm.com/v1/guardrails/content_safety"
)


def is_message_safe(payload: Dict[str, Any]) -> bool:
    """Send payload text to watsonx guardrails and return True if safe."""
    if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
        raise RuntimeError("WatsonX credentials missing")
    response = requests.post(
        CONTENT_SAFETY_ENDPOINT,
        json={"text": payload.get("message", "")},
        headers={
            "Authorization": f"Bearer {WATSONX_API_KEY}",
            "Content-Type": "application/json",
        },
    )
    response.raise_for_status()
    result = response.json()
    # Assume guardrails returns {"safe": true/false}
    return result.get("safe", False)


# Helper for batch safety check


def ensure_safe_batch(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    safe_messages = []
    for msg in messages:
        if is_message_safe(msg):
            safe_messages.append(msg)
    return safe_messages
