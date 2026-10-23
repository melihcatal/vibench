def normalize_caption(name, confidence):
    return {"text": name, "confidence": float(confidence)}


def normalize_text_blocks(blocks):
    return [
        {"text": block.get("DetectedText", ""), "confidence": float(block.get("Confidence", 0.0)) / 100.0}
        for block in blocks
        if block.get("DetectedText")
    ]


def normalize_safety_labels(labels):
    return [
        {"name": label.get("Name", ""), "confidence": float(label.get("Confidence", 0.0)) / 100.0, "parent": label.get("ParentName")}
        for label in labels
    ]
