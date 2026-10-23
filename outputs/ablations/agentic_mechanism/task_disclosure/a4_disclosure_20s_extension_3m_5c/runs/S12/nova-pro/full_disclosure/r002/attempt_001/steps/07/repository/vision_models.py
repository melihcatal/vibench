class ImageRequest:
    def __init__(self, image_data):
        self.image_data = image_data

class ImageResponse:
    def __init__(self, labels, text, safety_score):
        self.labels = labels
        self.text = text
        self.safety_score = safety_score

def normalize_labels(labels):
    return [label.lower() for label in labels]

def normalize_text(text):
    return text.lower()

def normalize_safety_score(score):
    return max(0, min(100, score))