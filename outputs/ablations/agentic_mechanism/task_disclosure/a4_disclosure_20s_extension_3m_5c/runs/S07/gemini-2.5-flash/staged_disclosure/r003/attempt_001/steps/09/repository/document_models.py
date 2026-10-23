import dataclasses
from typing import List, Dict, Any, Optional

@dataclasses.dataclass
class DocumentPage:
    page_number: int
    image_url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

@dataclasses.dataclass
class OCRRequest:
    document_id: str
    document_url: str
    pages: List[DocumentPage]

@dataclasses.dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float

@dataclasses.dataclass
class OCRToken:
    text: str
    bbox: BoundingBox
    confidence: Optional[float] = None

@dataclasses.dataclass
class OCRLine:
    text: str
    bbox: BoundingBox
    tokens: List[OCRToken]
    confidence: Optional[float] = None

@dataclasses.dataclass
class OCRBlock:
    bbox: BoundingBox
    lines: List[OCRLine]
    block_type: Optional[str] = None # e.g., "paragraph", "table", "image"

@dataclasses.dataclass
class OCRPageResult:
    page_number: int
    width: int
    height: int
    blocks: List[OCRBlock]
    full_text: Optional[str] = None

@dataclasses.dataclass
class OCRResponse:
    document_id: str
    page_results: List[OCRPageResult]
    
class OCRNormalizer:
    @staticmethod
    def normalize_bbox(bbox: Dict[str, Any]) -> BoundingBox:
        # Example normalization logic: ensure coordinates are floats
        return BoundingBox(
            x1=float(bbox.get("x1", 0)),
            y1=float(bbox.get("y1", 0)),
            x2=float(bbox.get("x2", 0)),
            y2=float(bbox.get("y2", 0))
        )

    @staticmethod
    def extract_full_text(page_results: List[OCRPageResult]) -> str:
        full_text_parts = []
        for page in page_results:
            for block in page.blocks:
                for line in block.lines:
                    full_text_parts.append(line.text)
            full_text_parts.append("\n--- Page End ---\n") # Separator between pages
        return "\n".join(full_text_parts).strip()
