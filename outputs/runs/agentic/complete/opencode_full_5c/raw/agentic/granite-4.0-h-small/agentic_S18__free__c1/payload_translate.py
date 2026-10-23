def translate_payload(payload: dict) -> dict:
    """Translate customer‑facing text fields in a message payload.

    Placeholder implementation – in a real service you could call a translation API.
    Provider identifier: This function shows where an external translation API would be integrated.
    """
    # Example: translate the 'message' field if it exists
    if "message" in payload and isinstance(payload["message"], str):
        # Simulated translation (replace with actual API call in production)
        payload["message"] = f"[Translated] {payload['message']}"
    return payload
