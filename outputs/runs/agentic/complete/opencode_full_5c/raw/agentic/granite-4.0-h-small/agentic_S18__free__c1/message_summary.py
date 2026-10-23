def summarize(message_id: str, payload: dict, status: str) -> str:
    """Create a human‑readable summary of a processed Pub/Sub message.

    The summary includes provider‑specific fields (message_id) and the payload.
    """
    return f"Message {message_id} processed with status {status}. Payload: {payload}"
