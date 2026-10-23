from messaging_models import normalize_payload, is_safe_content


def check_message_safety(payload: MessagePayload) -> bool:
    """Validate that the message payload text contains no unsafe content.

    Args:
        payload (MessagePayload): Normalized message.
    Returns:
        bool: True if safe, False otherwise.
    """
    # Example: check only top‑level string data fields
    if isinstance(payload.data, str):
        return is_safe_content(payload.data)
    # If data is a dict/list, perform shallow scan
    text = json.dumps(payload.data)
    return is_safe_content(text)


if __name__ == "__main__":
    # Demo
    sample = {"text": "This is a harmless message."}
    msg = normalize_payload({"data": sample, "attributes": {}})
    print("Safe?", check_message_safety(msg))
