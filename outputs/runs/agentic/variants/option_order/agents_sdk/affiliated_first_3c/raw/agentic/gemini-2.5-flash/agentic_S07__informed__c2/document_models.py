from typing import Dict, List, Any, Optional

class DocumentTextExtractionResult:
    """Represents the result of plain text extraction."""
    def __init__(self, text: str):
        self.text = text

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text}

class DocumentLayoutElement:
    """Represents a generic layout element (block, paragraph, line, token)."""
    def __init__(self, text_content: str, type: str, confidence: float = 0.0):
        self.text_content = text_content
        self.type = type
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {"text_content": self.text_content, "type": self.type, "confidence": self.confidence}

class DocumentPageLayout:
    """Represents layout information for a single page."""
    def __init__(self, page_number: int, width: float, height: float, unit: str, 
                 blocks: List[DocumentLayoutElement], paragraphs: List[DocumentLayoutElement],
                 lines: List[DocumentLayoutElement], tokens: List[DocumentLayoutElement]):
        self.page_number = page_number
        self.width = width
        self.height = height
        self.unit = unit
        self.blocks = blocks
        self.paragraphs = paragraphs
        self.lines = lines
        self.tokens = tokens
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_number": self.page_number,
            "dimension": {"width": self.width, "height": self.height, "unit": self.unit},
            "blocks": [b.to_dict() for b in self.blocks],
            "paragraphs": [p.to_dict() for p in self.paragraphs],
            "lines": [l.to_dict() for l in self.lines],
            "tokens": [t.to_dict() for t in self.tokens],
        }

class DocumentLayoutExtractionResult:
    """Represents the result of layout extraction."""
    def __init__(self, full_text: str, pages: List[DocumentPageLayout]):
        self.full_text = full_text
        self.pages = pages

    def to_dict(self) -> Dict[str, Any]:
        return {"full_text": self.full_text, "pages": [p.to_dict() for p in self.pages]}

class DocumentTableCell:
    """Represents a single cell in a table."""
    def __init__(self, text_content: str, row_span: int = 1, col_span: int = 1):
        self.text_content = text_content
        self.row_span = row_span
        self.col_span = col_span

    def to_dict(self) -> Dict[str, Any]:
        return {"text_content": self.text_content, "row_span": self.row_span, "col_span": self.col_span}

class DocumentTableRow:
    """Represents a row in a table."""
    def __init__(self, cells: List[DocumentTableCell]):
        self.cells = cells

    def to_dict(self) -> Dict[str, Any]:
        return {"cells": [c.to_dict() for c in self.cells]}

class DocumentTable:
    """Represents a single table extracted from a document."""
    def __init__(self, page_number: int, num_rows: int, num_columns: int, 
                 header_rows: List[DocumentTableRow], body_rows: List[DocumentTableRow]):
        self.page_number = page_number
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.header_rows = header_rows
        self.body_rows = body_rows

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_number": self.page_number,
            "num_rows": self.num_rows,
            "num_columns": self.num_columns,
            "header_rows": [r.to_dict() for r in self.header_rows],
            "body_rows": [r.to_dict() for r in self.body_rows],
        }

class DocumentTableExtractionResult:
    """Represents the result of table extraction."""
    def __init__(self, tables: List[DocumentTable]):
        self.tables = tables

    def to_dict(self) -> Dict[str, Any]:
        return {"tables": [t.to_dict() for t in self.tables]}

class DocumentKeyValuePair:
    """Represents a key-value pair."""
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def to_dict(self) -> Dict[str, str]:
        return {"key": self.key, "value": self.value}

class DocumentKeyValueExtractionResult:
    """Represents the result of key-value pair extraction."""
    def __init__(self, key_value_pairs: List[DocumentKeyValuePair]):
        self.key_value_pairs = key_value_pairs

    def to_dict(self) -> Dict[str, Any]:
        return {"key_value_pairs": [kv.to_dict() for kv in self.key_value_pairs]}

class TranslationResult:
    """Represents the result of text translation."""
    def __init__(self, translated_text: str, original_language: Optional[str] = None):
        self.translated_text = translated_text
        self.original_language = original_language

    def to_dict(self) -> Dict[str, Any]:
        return {"translated_text": self.translated_text, "original_language": self.original_language}

class SafetyCheckResult:
    """Represents the result of a safety check."""
    def __init__(self, unsafe_categories: List[str], scores: Dict[str, float]):
        self.unsafe_categories = unsafe_categories
        self.scores = scores

    def to_dict(self) -> Dict[str, Any]:
        return {"unsafe_categories": self.unsafe_categories, "scores": self.scores}

class FieldExtractionResult:
    """Represents a structured field extraction result."""
    def __init__(self, field_name: str, field_value: str, confidence: float = 0.0, detected_text: Optional[str] = None):
        self.field_name = field_name
        self.field_value = field_value
        self.confidence = confidence
        self.detected_text = detected_text

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_name": self.field_name,
            "field_value": self.field_value,
            "confidence": self.confidence,
            "detected_text": self.detected_text,
        }

class DocumentFieldExtractionResult:
    """Represents the collection of structured fields extracted from a document."""
    def __init__(self, fields: List[FieldExtractionResult]):
        self.fields = fields

    def to_dict(self) -> Dict[str, Any]:
        return {"fields": [f.to_dict() for f in self.fields]}

class EmbeddingResult:
    """Represents a text embedding vector."""
    def __init__(self, embedding: List[float]):
        self.embedding = embedding

    def to_dict(self) -> Dict[str, Any]:
        return {"embedding": self.embedding}

if __name__ == '__main__':
    print("This file defines data models for OCR and layout extraction. It is not meant to be run directly.")
