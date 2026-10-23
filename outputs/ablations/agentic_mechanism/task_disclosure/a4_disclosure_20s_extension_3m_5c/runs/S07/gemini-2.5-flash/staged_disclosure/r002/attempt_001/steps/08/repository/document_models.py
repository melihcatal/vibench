
class OcrRequest:
    """Represents a request for OCR processing."""
    def __init__(self, image_data: bytes, language: str = "en"):
        self.image_data = image_data
        self.language = language

class OcrResponse:
    """Represents a response from OCR processing."""
    def __init__(self, text_annotations: list, full_text: str):
        self.text_annotations = text_annotations
        self.full_text = full_text

class LayoutExtractionRequest:
    """Represents a request for layout extraction."""
    def __init__(self, document_data: bytes, features: list):
        self.document_data = document_data
        self.features = features

class LayoutExtractionResponse:
    """Represents a response from layout extraction."""
    def __init__(self, pages: list, entities: list):
        self.pages = pages
        self.entities = entities

def normalize_ocr_response(ocr_response: OcrResponse) -> dict:
    """Normalizes the OCR response into a standardized format."""
    normalized_data = {
        "full_text": ocr_response.full_text,
        "blocks": []
    }
    for annotation in ocr_response.text_annotations:
        normalized_data["blocks"].append({
            "text": annotation.get("description"),
            "bounds": annotation.get("boundingPoly")
        })
    return normalized_data

def normalize_layout_response(layout_response: LayoutExtractionResponse) -> dict:
    """Normalizes the layout extraction response into a standardized format."""
    normalized_data = {
        "pages": [],
        "document_entities": layout_response.entities
    }
    for page in layout_response.pages:
        normalized_data["pages"].append({
            "page_number": page.get("pageNumber"),
            "width": page.get("width"),
            "height": page.get("height"),
            "blocks": page.get("blocks")
        })
    return normalized_data
