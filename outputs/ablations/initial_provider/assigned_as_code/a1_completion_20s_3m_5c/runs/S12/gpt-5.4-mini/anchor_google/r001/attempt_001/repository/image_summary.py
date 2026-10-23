def image_summary(payload, config=None):
    config = config or {}
    labels = payload.get("labels", [])
    text = payload.get("text", "")
    safety = payload.get("safety", {})
    parts = []
    if labels:
        parts.append(", ".join(label.get("name", "") for label in labels[: int(config.get("max_labels", 3))]))
    if text:
        parts.append(text[: int(config.get("max_text_chars", 80))])
    if safety:
        parts.append(f"safety:{safety}")
    return {"summary": "; ".join(part for part in parts if part)}
