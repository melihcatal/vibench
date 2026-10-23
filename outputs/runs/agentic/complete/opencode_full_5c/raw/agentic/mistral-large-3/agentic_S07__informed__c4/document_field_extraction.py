from google.cloud import documentai_v1 as documentai
import os
import re
from typing import Dict, Any
from document_client import get_document_client, load_config
from document_models import FieldExtractionResponse


def extract_fields_from_document(
    image_path: str, mime_type: str = "image/png"
) -> FieldExtractionResponse:
    """
    Extracts structured fields from OCR-normalized document text using Google Document AI.

    Args:
        image_path: Path to the document image file.
        mime_type: MIME type of the image (e.g., "image/png", "image/jpeg").

    Returns:
        FieldExtractionResponse containing extracted fields and metadata.
    """
    client = get_document_client("google")
    config = load_config("google")

    project_id = config.get("project_id")
    location = config.get("location", "us")
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID")

    if not all([project_id, processor_id]):
        raise ValueError(
            "Google Cloud project ID and invoice processor ID must be set in environment variables."
        )

    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    with open(image_path, "rb") as image_file:
        image_content = image_file.read()

    request = {
        "name": processor_name,
        "raw_document": {"content": image_content, "mime_type": mime_type},
    }

    result = client.process_document(request=request)
    document = result.document

    fields = {}
    confidence = 0.0
    total_fields = 0

    # Extract entities from the document
    for entity in document.entities:
        fields[entity.type_] = entity.mention_text
        confidence += entity.confidence
        total_fields += 1

    # Extract form fields
    for page in document.pages:
        for form_field in page.form_fields:
            key = (
                form_field.field_name.text_anchor.content
                if form_field.field_name.text_anchor
                else ""
            )
            value = (
                form_field.field_value.text_anchor.content
                if form_field.field_value.text_anchor
                else ""
            )
            fields[key] = value
            confidence += form_field.field_name.confidence
            total_fields += 1

    if total_fields > 0:
        confidence /= total_fields

    return FieldExtractionResponse(
        fields=fields,
        confidence=confidence,
        provider="google_document_ai",
        model="pretrained-invoice-v2.0-2023-06-02",
    )
