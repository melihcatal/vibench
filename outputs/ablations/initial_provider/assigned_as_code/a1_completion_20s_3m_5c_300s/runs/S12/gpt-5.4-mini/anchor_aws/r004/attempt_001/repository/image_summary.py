import vision_models


def image_summary(payload, config=None):
    labels = vision_models.normalize_labels(payload.get("labels"))
    text = vision_models.normalize_text_detections(payload.get("text"))
    description = payload.get("description", "")
    parts = []
    if description:
        parts.append(description)
    if labels:
        parts.append("labels: " + ", ".join(item["name"] for item in labels[:5]))
    if text:
        parts.append("text: " + "; ".join(item["text"] for item in text[:3]))
    return {"summary": " | ".join(parts)}
