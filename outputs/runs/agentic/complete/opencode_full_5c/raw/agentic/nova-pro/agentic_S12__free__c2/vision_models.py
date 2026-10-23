def normalize_labels(labels):
    return [label["Name"] for label in labels]


def normalize_text_detections(detections):
    return [detection["DetectedText"] for detection in detections]


def normalize_moderation_labels(labels):
    return [label["Name"] for label in labels]
