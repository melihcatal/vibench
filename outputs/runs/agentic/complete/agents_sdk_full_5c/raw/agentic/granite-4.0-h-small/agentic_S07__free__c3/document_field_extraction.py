import os
from pydantic import BaseModel
from typing import List

# Payload model for the service that orchestrates OCR and downstream steps
class OCRJobInput(BaseModel):
    image_path: str
    target_lang: str = "en"
    safety_threshold: float = 0.5

# Normalized response bundle from the full OCR pipeline
class OCRJobOutput(BaseModel):
    extracted_text: str
    translated_text: str = None
    unsafe: bool = None
    field_extraction: dict = None
    embeddings: bytes = None

# Utility functions used by orchestrating code
def normalize_payload(payload: dict) -> OCRResponse:
    # Convert generic provider payload to our internal OCRResponse shape
    # This is where provider-specific logic lives (e.g., Azure vs. AWS vs. GCP)
    # For this scaffold we use Azure Form Recognizer (see document_client.py)
    blocks = [
        {
            "page": 1,
            "text": line["text"],
            "bbox": line["boundingBox"],
            "type": "line"
        }
        for line in payload.get("lines", [])
    ]
    return OCRResponse(blocks=blocks, raw_response=payload)

# Example orchestrator skeleton (not required but useful)
def run_full_pipeline(job: OCRJobInput) -> OCRJobOutput:
    client = DocumentClient()
    raw = client.extract_text(job.image_path)
    ocr_resp = normalize_payload(raw)
    text = " ".join([b["text"] for b in ocr_resp["blocks"]])
    result = OCRJobOutput(extracted_text=text)
    if job.target_lang:
        result.translated_text = translate_text(text, job.target_lang)
    result.unsafe = scan_for_unsafe(text) if job.safety_threshold else False
    # TODO: call field extraction & embedding steps
    return result
