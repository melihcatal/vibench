import dataclasses
from typing import List, Dict, Optional, Union

@dataclasses.dataclass
class OCRResult:
    text: str
    layout: Optional[Dict] = None
    tables: Optional[List[Dict]] = None
    key_values: Optional[Dict] = None

@dataclasses.dataclass
class LayoutElement:
    type: str
    content: str

@dataclasses.dataclass
class KeyValueEntry:
    key: str
    value: str

@dataclasses.dataclass
class DocumentFields:
    date: Optional[str] = None
    amount: Optional[str] = None
    vendor: Optional[str] = None
    total: Optional[str] = None

@dataclasses.dataclass
class NormalizedDocument:
    raw: bytes
    ocr: OCRResult
    fields: Optional[DocumentFields] = None
    translated: Optional[str] = None
    safe: Optional[bool] = None
    embeddings: Optional[List[float]] = None
