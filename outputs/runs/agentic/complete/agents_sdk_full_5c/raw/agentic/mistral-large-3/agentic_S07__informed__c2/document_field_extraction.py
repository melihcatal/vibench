from typing import Dict, Any, Optional
import os
from google.cloud import documentai_v1 as documentai
from document_models import FieldExtractionResponse


def extract_fields_from_document(gcs_uri: str, processor_id: str) -> FieldExtractionResponse:
    """Extract structured fields from OCR-normalized document text using Google Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    
    if not project_id or not processor_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID and processor_id must be provided."
        )
    
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    
    with open(gcs_uri.replace("gs://", ""), "rb") as f:
        document = {"content": f.read(), "mime_type": "application/pdf"}
    
    request = {"name": name, "raw_document": document}
    result = client.process_document(request=request)
    
    fields = {}
    for entity in result.document.entities:
        fields[entity.type_] = entity.mention_text
    
    return FieldExtractionResponse(fields=fields)