from typing import Any, Dict, List, Union


class OCRRequest:
    def __init__(self, image_path: str, language: str = 'eng'):
        self.image_path = image_path
        self.language = language


class OCRResponse:
    def __init__(self, text: str, confidence: float):
        self.text = text
        self.confidence = confidence


class LayoutExtractionRequest:
    def __init__(self, image_path: str):
        self.image_path = image_path


class LayoutExtractionResponse:
    def __init__(self, layout: Dict[str, Any]):
        self.layout = layout


def normalize_ocr_text(text: str) -> str:
    return text.strip().replace('\n', ' ').replace('  ', ' ')


def normalize_layout(layout: Dict[str, Any]) -> Dict[str, Any]:
    normalized_layout = {}
    for key, value in layout.items():
        if isinstance(value, str):
            normalized_layout[key] = value.strip()
        elif isinstance(value, list):
            normalized_layout[key] = [item.strip() for item in value]
        else:
            normalized_layout[key] = value
    return normalized_layout