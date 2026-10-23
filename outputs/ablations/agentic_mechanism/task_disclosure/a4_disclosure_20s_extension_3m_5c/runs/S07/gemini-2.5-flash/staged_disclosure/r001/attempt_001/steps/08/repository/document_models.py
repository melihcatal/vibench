import dataclasses
from typing import List, Dict, Any, Optional

# --- OCR Models ---

@dataclasses.dataclass
class OCRRequest:
    """Represents a request for OCR processing."""
    image_content: bytes
    language_hints: Optional[List[str]] = None
    
@dataclasses.dataclass
class Word:
    """Represents a detected word with its bounding box and text content."""
    text: str
    bounding_box: List[int] # [x_min, y_min, x_max, y_max]

@dataclasses.dataclass
class Line:
    """Represents a detected line of text."""
    words: List[Word]
    bounding_box: List[int] # [x_min, y_min, x_max, y_max]
    text: str

@dataclasses.dataclass
class OCRResponse:
    """Represents the response from an OCR processing operation."""
    full_text: str
    pages: List[Dict[str, Any]] # Placeholder for page-specific details, e.g., lines and words
    
# --- Layout Extraction Models ---

@dataclasses.dataclass
class TextBlock:
    """Represents a block of text with its content and bounding box."""
    text: str
    bounding_box: List[int] # [x_min, y_min, x_max, y_max]
    block_type: str # e.g., "paragraph", "heading", "list_item"

@dataclasses.dataclass
class LayoutExtractionRequest:
    """Represents a request for layout extraction."""
    image_content: bytes
    
@dataclasses.dataclass
class LayoutExtractionResponse:
    """Represents the response from a layout extraction operation."""
    text_blocks: List[TextBlock]
    page_dimensions: Optional[Dict[str, int]] = None # e.g., {"width": 1000, "height": 1500}

# --- Normalization Helpers ---

def normalize_ocr_response(raw_ocr_output: Dict[str, Any]) -> OCRResponse:
    """
    Normalizes a raw OCR service output into a standardized OCRResponse.
    This is a placeholder function; actual implementation would parse
    the specific OCR service's response format.
    """
    # Example placeholder implementation:
    full_text = raw_ocr_output.get("text", "")
    pages_data = raw_ocr_output.get("pages", [])
    
    return OCRResponse(full_text=full_text, pages=pages_data)

def normalize_layout_response(raw_layout_output: Dict[str, Any]) -> LayoutExtractionResponse:
    """
    Normalizes a raw layout extraction service output into a standardized LayoutExtractionResponse.
    This is a placeholder function; actual implementation would parse
    the specific layout extraction service's response format.
    """
    # Example placeholder implementation:
    text_blocks_data = []
    for block in raw_layout_output.get("blocks", []):
        text_blocks_data.append(
            TextBlock(
                text=block.get("text", ""),
                bounding_box=block.get("bbox", []),
                block_type=block.get("type", "paragraph")
            )
        )
    page_dims = raw_layout_output.get("page_dimensions")

    return LayoutExtractionResponse(text_blocks=text_blocks_data, page_dimensions=page_dims)
