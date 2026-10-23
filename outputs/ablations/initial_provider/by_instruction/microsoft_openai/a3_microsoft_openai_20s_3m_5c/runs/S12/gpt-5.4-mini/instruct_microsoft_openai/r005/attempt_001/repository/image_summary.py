from vision_models import normalize_labels, normalize_text


def image_summary(result):
    labels = normalize_labels(getattr(result, "labels", []))
    text = normalize_text(getattr(result, "text", []))
    description = getattr(result, "description", "")
    parts = []
    if description:
        parts.append(description)
    if labels:
        parts.append("Labels: " + ", ".join(labels))
    if text:
        parts.append("Text: " + ", ".join(text))
    return " | ".join(parts)
