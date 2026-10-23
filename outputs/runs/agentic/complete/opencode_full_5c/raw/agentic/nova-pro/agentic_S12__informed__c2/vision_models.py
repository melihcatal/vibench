class VisionRequest:
    def __init__(self, image_path, features):
        self.image_path = image_path
        self.features = features


class VisionResponse:
    def __init__(self, labels=None, description=None, text=None, safety_score=None):
        self.labels = labels
        self.description = description
        self.text = text
        self.safety_score = safety_score
