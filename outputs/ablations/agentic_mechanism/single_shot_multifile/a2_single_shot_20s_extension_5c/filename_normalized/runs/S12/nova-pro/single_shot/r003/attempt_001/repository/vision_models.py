class VisionRequest:
    def __init__(self, image_data, feature):
        self.image_data = image_data
        self.feature = feature

class VisionResponse:
    def __init__(self, annotations):
        self.annotations = annotations