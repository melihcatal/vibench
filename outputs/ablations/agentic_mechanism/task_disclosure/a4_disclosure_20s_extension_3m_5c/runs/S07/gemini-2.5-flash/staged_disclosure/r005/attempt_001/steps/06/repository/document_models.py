
class OcrRequest:
    def __init__(self, image_data: bytes, features: list):
        self.image_data = image_data
        self.features = features

class OcrResponse:
    def __init__(self, text_annotations: list, full_text_annotation: dict):
        self.text_annotations = text_annotations
        self.full_text_annotation = full_text_annotation

def normalize_ocr_response(response: OcrResponse) -> dict:
    """
    Normalizes the OCR response into a standardized dictionary format.
    """
    normalized_data = {
        "text_annotations": [
            {
                "description": annotation.description,
                "bounding_poly": annotation.bounding_poly
            }
            for annotation in response.text_annotations
        ],
        "full_text_annotation": response.full_text_annotation
    }
    return normalized_data

class LayoutExtractionRequest:
    def __init__(self, document_data: bytes, features: list):
        self.document_data = document_data
        self.features = features

class LayoutExtractionResponse:
    def __init__(self, pages: list):
        self.pages = pages

def normalize_layout_extraction_response(response: LayoutExtractionResponse) -> dict:
    """
    Normalizes the layout extraction response into a standardized dictionary format.
    """
    normalized_data = {
        "pages": [
            {
                "page_number": page.page_number,
                "blocks": page.blocks,
                "lines": page.lines,
                "words": page.words
            }
            for page in response.pages
        ]
    }
    return normalized_data
