class VisionRequest:
    def __init__(self, image_path):
        self.image_path = image_path

class VisionResponse:
    def __init__(self, labels=None, description=None, text=None, safety=None):
        self.labels = labels
        self.description = description
        self.text = text
        self.safety = safety