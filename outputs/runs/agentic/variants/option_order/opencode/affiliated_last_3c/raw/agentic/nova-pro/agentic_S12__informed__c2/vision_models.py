from typing import List


class VisionRequest:
    def __init__(self, image_path: str, features: List[str]):
        self.image_path = image_path
        self.features = features


class VisionResponse:
    def __init__(
        self, labels: List[str], description: str, text: List[str], safety: bool
    ):
        self.labels = labels
        self.description = description
        self.text = text
        self.safety = safety
