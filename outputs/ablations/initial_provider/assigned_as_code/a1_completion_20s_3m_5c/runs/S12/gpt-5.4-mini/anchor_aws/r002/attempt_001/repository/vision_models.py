from dataclasses import dataclass


def image_bytes(payload):
    return payload.get("image_bytes") if isinstance(payload, dict) else None


def text_value(payload, key, default=None):
    return payload.get(key, default) if isinstance(payload, dict) else default


def normalize_confidence(value):
    try:
        return float(value)
    except Exception:
        return 0.0


@dataclass
class VisionResult:
    value: dict
