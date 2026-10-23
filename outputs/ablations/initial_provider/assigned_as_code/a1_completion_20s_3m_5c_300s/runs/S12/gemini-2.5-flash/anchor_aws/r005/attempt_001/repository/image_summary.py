def image_summary(payload, config=None):
    config = config or {}
    summary_parts = []

    if "labels" in payload and payload["labels"]:
        label_names = [label["name"] for label in payload["labels"]]
        summary_parts.append(f"Detected objects and scenes: {', '.join(label_names)}.")

    if "description" in payload and payload["description"]:
        summary_parts.append(f"Generated description: {payload["description"]}")

    if "text_detections" in payload and payload["text_detections"]:
        detected_texts = [text["text"] for text in payload["text_detections"]]
        summary_parts.append(f"Detected text: '{', '.join(detected_texts)}'.")

    if "moderation_labels" in payload and payload["moderation_labels"]:
        moderation_issues = [label["name"] for label in payload["moderation_labels"]]
        summary_parts.append(f"Moderation issues detected: {', '.join(moderation_issues)}.")
    
    if not summary_parts:
        return {"summary": "No visual analysis results to summarize."}

    return {"summary": " ".join(summary_parts)}
