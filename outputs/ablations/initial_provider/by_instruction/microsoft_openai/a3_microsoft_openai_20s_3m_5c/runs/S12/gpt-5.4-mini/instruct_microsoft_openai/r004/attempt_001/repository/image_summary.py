from vision_models import normalize_text


def image_summary(labels, description, text):
    parts = []
    if labels:
        parts.append("Labels: " + ", ".join(labels))
    desc = normalize_text(description)
    if desc:
        parts.append("Description: " + desc)
    txt = normalize_text(text)
    if txt:
        parts.append("Text: " + txt)
    return " | ".join(parts)
