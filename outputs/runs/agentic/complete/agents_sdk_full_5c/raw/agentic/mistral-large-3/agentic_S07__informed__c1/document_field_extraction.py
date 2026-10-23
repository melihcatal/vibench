import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_models import FieldExtractionResponse


def extract_fields(document_path: str, mime_type: str) -> FieldExtractionResponse:
    """
    Extract structured fields from a document using Google Document AI Invoice Parser.
    """
    client = documentai.DocumentProcessorServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = "us"
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")  # Prebuilt invoice processor
    processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    with open(document_path, "rb") as document_file:
        document_data = document_file.read()

    request = {
        "name": processor_name,
        "raw_document": {
            "content": document_data,
            "mime_type": mime_type
        }
    }

    result = client.process_document(request=request)
    document = result.document

    fields = {}
    confidence_scores = {}

    for entity in document.entities:
        fields[entity.type_] = entity.mention_text
        confidence_scores[entity.type_] = entity.confidence

    return FieldExtractionResponse(
        fields=fields,
        confidence_scores=confidence_scores
    )