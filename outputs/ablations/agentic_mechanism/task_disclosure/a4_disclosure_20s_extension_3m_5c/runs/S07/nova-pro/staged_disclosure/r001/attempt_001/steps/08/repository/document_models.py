from typing import Any, Dict, List, Union


class OCRRequest:
    def __init__(self, image_path: str, language: str = 'en'):
        self.image_path = image_path
        self.language = language


class OCRResponse:
    def __init__(self, text: str, confidence: float):
        self.text = text
        self.confidence = confidence


class LayoutRequest:
    def __init__(self, image_path: str):
        self.image_path = image_path


class LayoutResponse:
    def __init__(self, elements: List[Dict[str, Any]]):
        self.elements = elements


def normalize_text(text: str) -> str:
    return text.strip().lower()


def normalize_layout(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized_elements = []
    for element in elements:
        normalized_element = {k.lower(): v for k, v in element.items()}
        normalized_elements.append(normalized_element)
    return normalized_elements