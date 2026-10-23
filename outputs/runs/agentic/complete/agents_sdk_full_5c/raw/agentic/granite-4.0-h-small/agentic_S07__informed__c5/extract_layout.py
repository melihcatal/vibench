import os
from document_client import get_mindee_client
from document_models import OcrResult

def extract_layout(image_path: str) -> OcrResult:
    """Extract layout elements (blocks, lines, tables) from a scanned document using Mindee Document OCR.
    Returns a structured layout object mirroring detected elements.
    """
    client = get_mindee_client()  # Provider identifier in code
    with open(image_path, "rb") as img_file:
        response = client.document_ocr.process(image=img_file)
    return OcrResult.from_mindee(response)
