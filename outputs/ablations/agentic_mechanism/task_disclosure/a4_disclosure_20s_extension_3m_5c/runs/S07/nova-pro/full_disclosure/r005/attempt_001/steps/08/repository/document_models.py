from typing import Any, Dict, List, Union

class OCRRequest:
    def __init__(self, document_path: str, language: str = 'en'):
        self.document_path = document_path
        self.language = language

class OCRResponse:
    def __init__(self, text: str, layout: Dict[str, Any]):
        self.text = text
        self.layout = layout

def normalize_text(text: str) -> str:
    return text.strip().lower()

def normalize_layout(layout: Dict[str, Any]) -> Dict[str, Any]:
    normalized_layout = {}
    for key, value in layout.items():
        normalized_layout[key.lower()] = value
    return normalized_layout