def normalize_label_response(response):
    return [{"name": label["Name"], "confidence": label["Confidence"] / 100.0} for label in response["Labels"]]


def normalize_text_response(response):
    return [text_detection["DetectedText"] for text_detection in response["TextDetections"]]


def normalize_safety_response(response):
    return response["ModerationLabels"][0]["Confidence"] / 100.0 if response["ModerationLabels"] else None