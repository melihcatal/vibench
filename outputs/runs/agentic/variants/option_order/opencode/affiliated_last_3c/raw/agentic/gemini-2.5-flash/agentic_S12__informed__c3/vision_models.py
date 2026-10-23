from typing import List, Dict, Any


class ImageRequest:
    def __init__(self, image_uri: str):
        self.image_uri = image_uri


class ImageLabelResponse:
    def __init__(self, labels: List[str]):
        self.labels = labels


class ImageDescriptionResponse:
    def __init__(self, description: str):
        self.description = description


class ImageTextResponse:
    def __init__(self, text: str):
        self.text = text


class ImageSafetyResponse:
    def __init__(self, safe_search_annotations: Dict[str, Any]):
        self.safe_search_annotations = safe_search_annotations
