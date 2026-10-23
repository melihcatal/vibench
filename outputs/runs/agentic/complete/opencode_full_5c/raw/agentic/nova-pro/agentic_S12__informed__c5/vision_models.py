def normalize_labels(labels):
    return [
        {"name": label["Name"], "confidence": label["Confidence"]} for label in labels
    ]


def normalize_text_detections(detections):
    return [
        {
            "detected_text": detection["DetectedText"],
            "confidence": detection["Confidence"],
        }
        for detection in detections
    ]


def normalize_moderation_labels(labels):
    return [
        {"name": label["Name"], "confidence": label["Confidence"]} for label in labels
    ]
