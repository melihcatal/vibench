def normalize_payload(payload):
    return {k: payload[k] for k in payload if payload[k] is not None}


def normalize_bytes_field(value):
    if isinstance(value, str):
        return value.encode("utf-8")
    return value


def make_key_ref(config):
    return {
        "project_id": config.get("project_id", ""),
        "location": config.get("location", "global"),
        "key_ring": config.get("key_ring", ""),
        "key_id": config.get("key_id", ""),
    }
