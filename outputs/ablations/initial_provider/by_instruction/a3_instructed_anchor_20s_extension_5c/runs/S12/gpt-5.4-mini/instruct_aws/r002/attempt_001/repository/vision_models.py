def normalize_labels(items):
    return [
        {"name": item.get("Name"), "confidence": float(item.get("Confidence", 0.0))}
        for item in items or []
    ]


def normalize_text(items):
    return [
        {"text": item.get("DetectedText"), "confidence": float(item.get("Confidence", 0.0))}
        for item in items or []
    ]


def normalize_safety(items):
    return [
        {
            "name": item.get("Name"),
            "parent_name": item.get("ParentName"),
            "confidence": float(item.get("Confidence", 0.0)),
        }
        for item in items or []
    ]
