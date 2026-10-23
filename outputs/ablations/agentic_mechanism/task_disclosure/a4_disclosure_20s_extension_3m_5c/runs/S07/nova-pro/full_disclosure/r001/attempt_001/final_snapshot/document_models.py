from typing import Dict, List, Union


class OCRRequest:
    def __init__(self, document_bytes: bytes):
        self.document_bytes = document_bytes


class OCRResponse:
    def __init__(self, text: str, blocks: List[Dict]):
        self.text = text
        self.blocks = blocks


class LayoutRequest:
    def __init__(self, document_bytes: bytes):
        self.document_bytes = document_bytes


class LayoutResponse:
    def __init__(self, blocks: List[Dict]):
        self.blocks = blocks


def normalize_text(text: str) -> str:
    return text.strip()


def normalize_blocks(blocks: List[Dict]) -> List[Dict]:
    normalized_blocks = []
    for block in blocks:
        if block['BlockType'] == 'LINE':
            normalized_blocks.append({
                'Text': normalize_text(block['Text']),
                'Geometry': block['Geometry']
            })
    return normalized_blocks