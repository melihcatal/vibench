from typing import Any, Dict, List, Union

class OCRRequest:
    def __init__(self, image_path: str):
        self.image_path = image_path

class OCRResponse:
    def __init__(self, text: str):
        self.text = text

class LayoutRequest:
    def __init__(self, image_path: str):
        self.image_path = image_path

class LayoutResponse:
    def __init__(self, elements: List[Dict[str, Any]]):
        self.elements = elements

def normalize_text(text: str) -> str:
    return text.strip().lower()

def normalize_layout(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return elements