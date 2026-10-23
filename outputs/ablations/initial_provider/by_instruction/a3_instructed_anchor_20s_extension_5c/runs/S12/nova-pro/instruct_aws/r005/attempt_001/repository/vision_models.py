def normalize_labels(labels):
    return [{'Name': label['Name'], 'Confidence': label['Confidence']} for label in labels]

def normalize_text_detections(detections):
    return [{'DetectedText': detection['DetectedText'], 'Confidence': detection['Confidence']} for detection in detections]

def normalize_moderation_labels(labels):
    return [{'Name': label['Name'], 'Confidence': label['Confidence']} for label in labels]