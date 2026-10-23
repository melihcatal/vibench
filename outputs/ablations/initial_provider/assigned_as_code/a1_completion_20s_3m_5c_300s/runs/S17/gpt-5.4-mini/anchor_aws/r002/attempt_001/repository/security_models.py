def _get_value(payload, *keys):
    for key in keys:
        if isinstance(payload, dict) and key in payload:
            return payload[key]
    return None


def normalize_plaintext_payload(payload):
    plaintext = _get_value(payload, "plaintext", "plain_text", "text")
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()
    return {"plaintext": plaintext}


def normalize_ciphertext_payload(payload):
    ciphertext = _get_value(payload, "ciphertext", "cipher_text")
    return {"ciphertext": ciphertext}


def normalize_message_payload(payload):
    message = _get_value(payload, "message", "data")
    if isinstance(message, str):
        message = message.encode()
    return {
        "message": message,
        "signature": _get_value(payload, "signature"),
        "operation": _get_value(payload, "operation", "action"),
    }
