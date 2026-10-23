from typing import List, Dict, Optional, TypedDict
from dataclasses import dataclass
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    LINE = "line"
    WORD = "word"
    TABLE = "table"
    CELL = "cell"
    KEY_VALUE = "key_value"
    SELECTION_MARK = "selection_mark"


@dataclass
class BoundingBox:
    vertices: List[Dict[str, float]]  # [{"x": float, "y": float}]


@dataclass
class DocumentBlock:
    block_type: BlockType
    text: Optional[str] = None
    bounding_box: Optional[BoundingBox] = None
    confidence: Optional[float] = None
    children: Optional[List['DocumentBlock']] = None


@dataclass
class DocumentTable:
    rows: int
    cols: int
    cells: List[Dict]
    bounding_box: Optional[BoundingBox] = None


@dataclass
class KeyValuePair:
    key: DocumentBlock
    value: DocumentBlock
    confidence: Optional[float] = None


@dataclass
class OcrResponse:
    text: str
    blocks: List[DocumentBlock]
    tables: List[DocumentTable]
    key_value_pairs: List[KeyValuePair]
    confidence: Optional[float] = None


class AzureDocumentIntelligenceModels:
    READ = "prebuilt-read"
    LAYOUT = "prebuilt-layout"
    INVOICE = "prebuilt-invoice"
    RECEIPT = "prebuilt-receipt"


class GoogleDocumentAIProcessors:
    OCR_PROCESSOR = "ocr"
    FORM_PARSER = "form-parser"
    INVOICE_PROCESSOR = "invoice-processor"