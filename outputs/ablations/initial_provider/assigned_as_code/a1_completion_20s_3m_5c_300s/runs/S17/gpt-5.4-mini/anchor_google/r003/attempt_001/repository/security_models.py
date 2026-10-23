def normalize_bytes(value):
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    return bytes(value)


def normalize_payload(payload):
    payload = dict(payload or {})
    for key in ("plaintext", "ciphertext", "data_key", "signature", "digest", "encrypted_payload"):
        if key in payload:
            payload[key] = normalize_bytes(payload[key])
    return payload
