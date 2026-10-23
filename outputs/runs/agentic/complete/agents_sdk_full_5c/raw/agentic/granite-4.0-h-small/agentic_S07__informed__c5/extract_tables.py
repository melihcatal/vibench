import os
from document_client import get_mindee_client
from document_models import OcrResult

def extract_tables(image_path: str) -> OcrResult:
    """Extract tables from a scanned document using Mindee Document OCR.
    Returns a structure with table rows, headers and cell values.
    """
    client = get_mindee_client()  # Provider identifier in code
    with open(image_path, "rb") as img_file:
        response = client.document_ocr.process(image=img_file)
    # Convert the OCR response to our local table model
    return OcrResult.from_mindee(response)
