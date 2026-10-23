
class OcrRequest:
    def __init__(self, image_path: str):
        self.image_path = image_path

class OcrResponse:
    def __init__(self, text: str, bounding_boxes: list):
        self.text = text
        self.bounding_boxes = bounding_boxes

class LayoutExtractionRequest:
    def __init__(self, image_path: str, features: list):
        self.image_path = image_path
        self.features = features

class LayoutExtractionResponse:
    def __init__(self, layout_elements: dict):
        self.layout_elements = layout_elements

def normalize_text(text: str) -> str:
    """Normalizes extracted text."""
    return text.strip().lower()
