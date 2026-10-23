from dataclasses import dataclass


def normalize_image_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"image_bytes": payload}


def normalize_text_items(items):
    return [{"text": item.get("text", ""), "confidence": float(item.get("confidence", 0.0))} for item in items or []]


def normalize_label_items(items):
    return [{"name": item.get("name", ""), "confidence": float(item.get("confidence", 0.0))} for item in items or []]


def normalize_safety_items(items):
    return [{"label": item.get("label", ""), "confidence": float(item.get("confidence", 0.0)), "unsafe": bool(item.get("unsafe", False))} for item in items or []]


@dataclass
class VisionRequest:
    payload: dict
    config: dict | None = None


@dataclass
class VisionResponse:
    data: dict
