from vision_models import normalize_label_items, normalize_text_items


def image_summary(payload, config=None):
    labels = normalize_label_items(payload.get("labels", []))
    text = normalize_text_items(payload.get("text", []))
    parts = []
    if labels:
        parts.append(", ".join(item["name"] for item in labels[:3]))
    if text:
        parts.append("text: " + ", ".join(item["text"] for item in text[:2]))
    return {"summary": "; ".join(parts)}
