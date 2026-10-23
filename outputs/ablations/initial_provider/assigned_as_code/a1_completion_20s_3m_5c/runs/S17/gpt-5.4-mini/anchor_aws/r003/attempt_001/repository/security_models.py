def normalize_bytes(value):
    if value is None:
        return None
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    return bytes(value)


def normalize_payload(payload):
    payload = payload or {}
    normalized = dict(payload)
    for key in ("plaintext", "ciphertext", "message", "signature"):
        if key in normalized:
            normalized[key] = normalize_bytes(normalized[key])
    return normalized
