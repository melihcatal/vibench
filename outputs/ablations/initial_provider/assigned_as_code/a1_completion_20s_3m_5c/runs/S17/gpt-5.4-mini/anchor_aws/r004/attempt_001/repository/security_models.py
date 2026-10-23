def normalize_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"plaintext": payload}


def normalize_ciphertext(payload):
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"ciphertext": payload}


def response_item(kind, value):
    return {kind: value}
