from typing import List, Dict, Any

class ImageLabelsRequest:
    def __init__(self, image_content: bytes):
        self.image_content = image_content

class ImageLabel:
    def __init__(self, description: str, score: float):
        self.description = description
        self.score = score

class ImageLabelsResponse:
    def __init__(self, labels: List[ImageLabel]):
        self.labels = labels
