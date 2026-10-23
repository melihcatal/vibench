from dataclasses import dataclass
from typing import List, Dict

class OcrBlock:
    def __init__(self, text: str, confidence: float, page: int, block_type: str):
        self.text = text
        self.confidence = confidence
        self.page = page
        self.type = block_type

class OcrLine:
    def __init__(self, text: str, confidence: float, block_id: str):
        self.text = text
        self.confidence = confidence
        self.block_id = block_id

class OcrTable:
    def __init__(self, rows: List[List[str]], headers: List[str] = None):
        self.rows = rows
        self.headers = headers or []

class OcrResult:
    def __init__(self, text: str, blocks: List[OcrBlock] = [], lines: List[OcrLine] = [], tables: List[OcrTable] = []):
        self.full_text = text
        self.blocks = blocks
        self.lines = lines
        self.tables = tables
        self.confidence = sum(b.confidence for b in blocks) / len(blocks) if blocks else 0.0

    @classmethod
    def from_mindee(cls, mindee_response):
        # Simplified extraction - real implementation should iterate pages and blocks
        full_text = " ".join(page.get('raw_text', '') for page in mindee_response.pages)
        blocks = [OcrBlock(page.get('raw_text', ''), page.get('confidence', 0.0), page.get('page'), 'block')
                  for page in mindee_response.pages]
        lines = []  # Populate if needed
        tables = []  # Populate if needed
        return cls(full_text, blocks, lines, tables)
