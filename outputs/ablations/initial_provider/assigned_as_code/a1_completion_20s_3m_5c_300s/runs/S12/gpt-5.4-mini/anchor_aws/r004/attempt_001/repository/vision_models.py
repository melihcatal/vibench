def image_bytes_from_payload(payload):
    return payload.get("image_bytes") or payload.get("bytes")


def normalize_labels(labels):
    return [{"name": item.get("name"), "confidence": float(item.get("confidence", 0.0))} for item in labels or []]


def normalize_text_detections(detections):
    return [{"text": item.get("text"), "confidence": float(item.get("confidence", 0.0))} for item in detections or []]


def normalize_safety_labels(labels):
    return [{"name": item.get("name"), "confidence": float(item.get("confidence", 0.0))} for item in labels or []]


def build_analysis_result(**items):
    return items
