
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class DocumentText:
    text: str

@dataclass
class DocumentLayoutBlock:
    text: str
    bounding_boxes: List[float] # [x1, y1, x2, y2, ...]

@dataclass
class DocumentTable:
    rows: List[List[str]]
    bounding_boxes: List[float]

@dataclass
class DocumentKeyValue:
    key: str
    value: str
    key_bounding_boxes: List[float]
    value_bounding_boxes: List[float]

@dataclass
class DocumentExtractionResult:
    text_content: str = ""
    layout_blocks: List[DocumentLayoutBlock] = field(default_factory=list)
    tables: List[DocumentTable] = field(default_factory=list)
    key_values: List[DocumentKeyValue] = field(default_factory=list)
    
@dataclass
class DocumentTranslation:
    translated_text: str
    
@dataclass
class DocumentSafetyResult:
    is_safe: bool
    reasons: List[str]

@dataclass
class DocumentField:
    field_name: str
    field_value: str

@dataclass
class DocumentEmbedding:
    embedding_vector: List[float]
