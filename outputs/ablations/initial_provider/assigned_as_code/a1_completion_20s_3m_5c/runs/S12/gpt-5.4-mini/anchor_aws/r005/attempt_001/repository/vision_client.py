import os


def load_config(config=None):
    cfg = dict(config or {})
    if "region" not in cfg:
        cfg["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return cfg


def image_bytes_from_payload(payload):
    if isinstance(payload, dict) and "image_bytes" in payload:
        return payload["image_bytes"]
    if isinstance(payload, dict) and "bytes" in payload:
        return payload["bytes"]
    return payload
