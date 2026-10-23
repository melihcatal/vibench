import os
from mindee import MindeeClient
from document_models import OcrResult

def extract_text(image_path: str) -> OcrResult:
    """Extract plain text from a scanned document image using Mindee Document OCR.
    Returns a structured OcrResult containing full extracted text and confidence metadata.
    """
    client = get_mindee_client()  # Provider identifier in code
    with open(image_path, "rb") as img_file:
        response = client.document_ocr.process(image=img_file)
    # Normalise response to our local model
    return OcrResult.from_mindee(response)
