import os


def load_vision_config(config=None):
    merged = {}
    merged.update({
        "region": os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "max_labels": 10,
        "max_text_detections": 50,
    })
    if config:
        merged.update(config)
    return merged


def load_image_bytes(payload):
    if isinstance(payload, dict):
        return payload.get("image_bytes")
    return payload
