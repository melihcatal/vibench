from pydantic import BaseModel, Field
from typing import List, Dict, Any


class DocumentBlock(BaseModel):
    page_number: int = Field(..., description="Page index starting at 1")
    bbox: List[float] = Field(
        ..., description="Bounding box [x, y, width, height] relative to page"
    )
    text: str = Field(..., description="Recognized text")
    confidence: float = Field(..., description="Confidence score")


class DocumentLine(BaseModel):
    blocks: List[DocumentBlock] = Field(
        ..., description="Ordered list of blocks in the line"
    )


class DocumentTable(BaseModel):
    rows: List[List[DocumentBlock]] = Field(..., description="2‑D list of cell blocks")
    headers: List[DocumentBlock] = Field(..., description="Header row (optional)")


class DocumentRegion(BaseModel):
    type: str = Field(
        ..., description="Region type: 'block', 'line', 'table', 'key_value', etc."
    )
    data: Any = Field(
        ...,
        description="Union type containing appropriate model (Block, Line, Table, etc.)",
    )


class OCRRequest(BaseModel):
    document_id: str = Field(
        ..., description="Unique identifier for the scanned image / document"
    )
    image_bytes: bytes = Field(..., description="Base64‑encoded image data")
    image_format: str = Field(
        ..., description="Format of the image, e.g., 'jpeg', 'png' or a content type"
    )


class OCRResponse(BaseModel):
    document_id: str = Field(..., description="Original document identifier")
    detected_text: List[DocumentBlock] = Field(
        ..., description="All recognized blocks across pages"
    )
    layout: List[DocumentRegion] = Field(
        ..., description="Structured layout elements (lines, tables, etc.)"
    )
