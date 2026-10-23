from typing import Any, Dict, List


class OCRRequest:
    def __init__(self, image_path: str, language: str = 'en'):
        self.image_path = image_path
        self.language = language


class OCRResponse:
    def __init__(self, text: str, confidence: float):
        self.text = text
        self.confidence = confidence


class LayoutRequest:
    def __init__(self, image_path: str, language: str = 'en'):
        self.image_path = image_path
        self.language = language


class LayoutResponse:
    def __init__(self, blocks: List[Dict[str, Any]]):
        self.blocks = blocks


def normalize_text(text: str) -> str:
    return text.strip().lower()


def normalize_layout(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized_blocks = []
    for block in blocks:
        normalized_block = {
            'type': block.get('type', '').lower(),
            'text': normalize_text(block.get('text', '')),
            'confidence': block.get('confidence', 0.0),
        }
        normalized_blocks.append(normalized_block)
    return normalized_blocks
