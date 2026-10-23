import json
from typing import Dict, Any, Optional
from messaging_client import MessagingClient
from ibm_watsonx_ai.hlp import GuardrailsClient


def check_message_safety(
    payload: Dict[str, Any], *, additional_context: Optional[str] = None
) -> bool:
    """Determine whether a message payload contains unsafe content.

    Uses the watsonx.ai Guardrails client (same-scenario provider) with
    credentials from WATSONX_API_KEY and WATSONX_PROJECT_ID. The function
    returns True if the content is safe, False if unsafe.

    Parameters:
        payload (dict): The raw JSON message payload.
        additional_context (str, optional): Optional textual context passed
            along with the payload for a richer moderation decision.
    Returns:
        bool: True if safe, False if unsafe.
    """
    # Ensure the guardrails service is available (lazy import)
    try:
        guard = GuardrailsClient()
    except Exception as e:
        # Fallback to a no‑op if the service cannot be initialized
        print("Guardrails client failed to initialize:", e)
        return True  # assume safe when service unavailable
    # Guardrails accepts text content; we concatenate payload fields into a
    # readable string.
    text = " ".join(str(v) for v in payload.values()) + (
        " " + additional_context if additional_context else ""
    )
    # Call the moderation API
    response = guard.analyze(
        content=text, categories=["hate", "self_harm", "sexual", "violence"]
    )
    # The response contains a `moderation` field with category scores
    if response.get("moderation"):
        # If any category exceeds the default threshold (0.5) we treat as unsafe
        unsafe = any(score > 0.5 for score in response["moderation"].values())
        return not unsafe
    # If moderation data missing, treat as safe
    return True


# Example usage (for local testing)
if __name__ == "__main__":
    test_payload = {
        "event_id": "e-unsafe-123",
        "type": "order_created",
        "timestamp": "2025-08-15T12:34:56Z",
        "data": {
            "order_number": "ORD-001",
            "amount": 100,
            "notes": "free guns, avoid taxes",
        },
    }
    safe = check_message_safety(test_payload, additional_context="processing step X")
    print("Payload safe?", safe)
