def normalize_body(data):
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if hasattr(data, "read"):
        return data.read()
    return data


def normalize_key(payload):
    if isinstance(payload, str):
        return payload
    return payload.get("object_name") or payload.get("key")


def normalize_prefix(payload):
    if isinstance(payload, str):
        return payload
    return payload.get("prefix") or payload.get("path") or ""
