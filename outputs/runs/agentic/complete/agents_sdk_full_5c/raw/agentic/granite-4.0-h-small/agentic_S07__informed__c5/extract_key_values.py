import os
from mindee import MindeeClient
from document_models import OcrResult

def extract_key_values(image_path: str) -> dict:
    """Extract key‑value pairs from a form‑like document using Mindee Document OCR.
    Returns a flat dictionary mapping each detected key to its value.
    """
    client = get_mindee_client()  # Provider identifier in code
    with open(image_path, "rb") as img_file:
        response = client.document_ocr.process(image=img_file)
    # Mindee does not expose a dedicated key‑value endpoint.
    # As a simple example we re‑use the text extraction and apply a naive pairing.
    result = OcrResult.from_mindee(response)
    kv = {}
    lines = result.lines
    i = 0
    while i < len(lines) - 1:
        if lines[i].text.endswith(':'):
            kv[lines[i].text.rstrip(':')] = lines[i + 1].text.strip()
            i += 2
        else:
            i += 1
    return kv
