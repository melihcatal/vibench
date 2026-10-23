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


def normalize_ocr_response(response: OCRResponse) -> str:
    return response.text.strip()


def normalize_layout_response(response: LayoutResponse) -> List[Dict[str, Any]]:
    normalized_elements = []
    for element in response.elements:
        normalized_element = {
            'type': element['type'],
            'text': element['text'].strip() if 'text' in element else '',
            'bbox': element['bbox']
        }
        normalized_elements.append(normalized_element)
    return normalized_elements