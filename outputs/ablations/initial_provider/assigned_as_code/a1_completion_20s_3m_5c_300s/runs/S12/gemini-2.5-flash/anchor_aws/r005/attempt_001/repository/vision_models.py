def normalize_labels(labels_response):
    return [
        {"name": label["Name"], "confidence": label["Confidence"] / 100.0}
        for label in labels_response.get("Labels", [])
    ]

def normalize_text_detections(text_response):
    return [
        {"text": text["DetectedText"], "confidence": text["Confidence"] / 100.0, "type": text["Type"]}
        for text in text_response.get("TextDetections", [])
    ]

def normalize_moderation_labels(moderation_response):
    return [
        {"name": label["ParentName"] + ": " + label["Name"] if label.get("ParentName") else label["Name"], "confidence": label["Confidence"] / 100.0}
        for label in moderation_response.get("ModerationLabels", [])
    ]
