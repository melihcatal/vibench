from vision_models import normalize_description_response


def image_summary(payload, config=None):
    labels = payload.get("labels", [])
    description = payload.get("description", "")
    parts = []
    if description:
        parts.append(description)
    if labels:
        parts.append(", ".join(label.get("name", "") for label in labels[:5]))
    return normalize_description_response({"description": "; ".join(parts)})
