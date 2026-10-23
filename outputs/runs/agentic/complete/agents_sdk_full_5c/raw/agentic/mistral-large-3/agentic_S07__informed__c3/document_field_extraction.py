from google.cloud import documentai_v1 as documentai
from typing import Dict, Any
import os
from document_models import FieldExtractionResponse


def extract_fields_from_document(gcs_uri: str) -> FieldExtractionResponse:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")

    if not project_id or not processor_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID and GOOGLE_DOCUMENT_AI_PROCESSOR_ID "
            "must be set in the environment."
        )

    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(project_id, location, processor_id)

    request = {
        "name": processor_name,
        "raw_document": {
            "gcs_uri": gcs_uri,
            "mime_type": "application/pdf"
        }
    }

    result = client.process_document(request=request)
    document = result.document

    fields = {}
    for entity in document.entities:
        fields[entity.type_] = {
            "value": entity.mention_text,
            "confidence": entity.confidence
        }

    return FieldExtractionResponse(
        fields=fields,
        confidence=document.entity_extraction_confidence
    )