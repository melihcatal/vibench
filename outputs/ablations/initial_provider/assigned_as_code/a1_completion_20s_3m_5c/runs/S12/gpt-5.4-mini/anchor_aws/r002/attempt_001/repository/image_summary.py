def image_summary(payload, config=None):
    labels = payload.get("labels", []) if isinstance(payload, dict) else []
    texts = payload.get("text", []) if isinstance(payload, dict) else []
    description = payload.get("description", "") if isinstance(payload, dict) else ""
    parts = [description] if description else []
    if labels:
        parts.append("labels: " + ", ".join(label.get("name", "") for label in labels if isinstance(label, dict)))
    if texts:
        parts.append("text: " + " ".join(texts))
    return {"summary": "; ".join(part for part in parts if part)}
