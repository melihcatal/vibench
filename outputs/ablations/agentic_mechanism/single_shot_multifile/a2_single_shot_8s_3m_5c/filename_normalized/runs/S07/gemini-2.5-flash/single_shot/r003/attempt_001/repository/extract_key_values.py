import os
from typing import List, Optional

from google.cloud import documentai_v1 as documentai

from document_client import get_gcp_documentai_processor_path
from document_models import DocumentInput, KeyValueExtractionOutput, KeyValuePair

def extract_document_key_values(
    document_input: DocumentInput,
    processor_id: Optional[str] = None,
) -> KeyValueExtractionOutput:
    """Extracts key-value pairs from a form-like document using Google Cloud Document AI's Form Parser."""
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us")
    # Use Form Parser or a specialized custom processor for key-value extraction.
    default_processor_id = os.environ.get("GCP_DOCUMENTAI_FORM_PROCESSOR_ID", "FORM_PARSER_PROCESSOR_ID_HERE")

    processor_name = get_gcp_documentai_processor_path(
        project_id, location, processor_id or default_processor_id
    )

    client = documentai.DocumentProcessorServiceClient()

    raw_document = documentai.RawDocument(
        content=document_input.image_bytes,
        mime_type=document_input.mime_type,
    )
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    extracted_key_values: List[KeyValuePair] = []

    for entity in document.entities:
        if entity.type and entity.mention_text and entity.normalized_value.text:
            key = documentai.get_text_anchor_text(entity.text_anchor, document.text)
            value = entity.normalized_value.text or documentai.get_text_anchor_text(entity.text_anchor, document.text)
            if key and value:
                extracted_key_values.append(KeyValuePair(key=key.strip(), value=value.strip()))

    return KeyValueExtractionOutput(pairs=extracted_key_values)
