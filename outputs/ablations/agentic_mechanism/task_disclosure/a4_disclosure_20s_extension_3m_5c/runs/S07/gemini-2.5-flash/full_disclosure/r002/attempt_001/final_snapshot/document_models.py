
import dataclasses
from typing import List, Optional, Any

@dataclasses.dataclass
class OcrRequest:
    """
    Represents a request for Optical Character Recognition (OCR).
    """
    image_base64: str
    language_hints: Optional[List[str]] = None

@dataclasses.dataclass
class OcrResponse:
    """
    Represents the response from an OCR operation.
    """
    text: str
    pages: List[Any]  # Placeholder for detailed page/block/line information

@dataclasses.dataclass
class LayoutExtractionRequest:
    """
    Represents a request for layout extraction.
    """
    ocr_response: OcrResponse
    features: Optional[List[str]] = None  # e.g., ["tables", "forms", "blocks"]

@dataclasses.dataclass
class LayoutExtractionResponse:
    """
    Represents the response from a layout extraction operation.
    """
    extracted_elements: List[Any]  # Placeholder for structured layout elements

class NormalizationHelper:
    """
    Provides utility methods for normalizing OCR and layout extraction data.
    """
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalizes extracted text (e.g., removing extra spaces, handling line breaks).
        """
        return " ".join(text.split()).strip()

    @staticmethod
    def post_process_layout_elements(elements: List[Any]) -> List[Any]:
        """
        Applies post-processing rules to layout elements for consistency.
        """
        # Example: Could sort elements, merge overlapping ones, etc.
        return elements

