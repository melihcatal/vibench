from vision_models import build_result


def image_summary(labels, description, text):
    parts = []
    if getattr(labels, "items", None):
        parts.append("Labels: " + ", ".join(labels.items))
    if getattr(description, "text", None):
        parts.append("Description: " + description.text)
    if getattr(text, "text", None):
        parts.append("Text: " + text.text)
    return build_result(text="\n".join(parts), items=getattr(labels, "items", []))
