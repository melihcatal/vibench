import json
import spacy
from document_models import FieldExtractionRequest, FieldExtractionResponse
from document_client import DocumentClient

def extract_fields(text: str, schema: dict) -> FieldExtractionResponse:
    """Extract structured fields from OCR-normalized text using spaCy and a JSON schema.",
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    extracted = {}
    for key, expected_type in schema.items():
        # Simple heuristic: look for an exact token match to the key name
        for ent in doc.ents:
            if ent.text.lower() == key.lower():
                extracted[key] = ent.text
                break
    # Ensure all required fields are present (missing = None)
    for key in schema:
        if key not in extracted:
            extracted[key] = None
    return FieldExtractionResponse(extracted_fields=extracted)


def field_extraction_pipeline(image_path: str, schema_path: str) -> FieldExtractionResponse:
    """End-to-end extraction: OCR -> field extraction.",
    client = DocumentClient(service="azure_ocr")
    with open(image_path, "rb") as img:
        ocr_result = client.ocr_image(image_bytes=img.read())
        ocr_text = ocr_result.get("text", "")
    with open(schema_path, "r") as sch:
        schema = json.load(sch)
    return extract_fields(ocr_text, schema)
