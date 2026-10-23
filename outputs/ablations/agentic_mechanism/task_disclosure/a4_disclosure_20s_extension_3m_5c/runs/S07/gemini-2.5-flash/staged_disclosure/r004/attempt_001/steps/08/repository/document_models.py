from typing import List, Optional, Any
from pydantic import BaseModel, Field

class OcrPage(BaseModel):
    page_number: int
    text_content: str
    words: List[Any] = []
    lines: List[Any] = []

class OcrOutput(BaseModel):
    pages: List[OcrPage]
    full_text: str

class LayoutPage(BaseModel):
    page_number: int
    elements: List[Any] = []

class LayoutOutput(BaseModel):
    pages: List[LayoutPage]

class DocumentUnderstandingResponse(BaseModel):
    ocr_output: Optional[OcrOutput] = None
    layout_output: Optional[LayoutOutput] = None

class DocumentUnderstandingRequest(BaseModel):
    document_url: str
    perform_ocr: bool = False
    extract_layout: bool = False

def normalize_text(text: str) -> str:
    """Normalizes text by removing extra whitespace and special characters."""
    return " ".join(text.split()).strip()

def extract_text_from_ocr_output(ocr_output: OcrOutput) -> str:
    """Extracts and concatenates text content from all pages in OCR output."""
    return "\n".join([page.text_content for page in ocr_output.pages])

