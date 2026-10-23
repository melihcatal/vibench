from vision_models import normalize_items


def image_summary(payload, config=None):
    config = config or {}
    labels = normalize_items(payload.get("labels", []))
    text = payload.get("text", "")
    parts = [item["text"] for item in labels[: int(config.get("max_labels", 3))] if item.get("text")]
    summary = "; ".join(parts)
    if text:
        summary = f"{summary} | OCR: {text}" if summary else f"OCR: {text}"
    return {"summary": summary}
