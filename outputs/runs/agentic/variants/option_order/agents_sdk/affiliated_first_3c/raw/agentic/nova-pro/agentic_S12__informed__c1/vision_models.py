class VisionRequest:
    def __init__(self, image_path):
        self.image_path = image_path

class VisionResponse:
    def __init__(self, annotations):
        self.annotations = annotations