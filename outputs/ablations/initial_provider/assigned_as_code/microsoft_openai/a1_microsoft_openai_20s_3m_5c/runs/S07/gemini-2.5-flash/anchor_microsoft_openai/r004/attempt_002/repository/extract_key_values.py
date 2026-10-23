import os
from google.cloud import documentai_v1 as documentai
from document_client import DocumentClient
from document_models import DocumentInput, ExtractedKeyValues

def extract_key_values(document_input: DocumentInput, config: dict = None) -> ExtractedKeyValues:
    config = config or {}
    project_id = config.get("GOOGLE_CLOUD_PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = config.get("GOOGLE_CLOUD_LOCATION") or os.environ.get("GOOGLE_CLOUD_LOCATION", "us") # e.g., "us"
    processor_id = config.get("GOOGLE_CLOUD_DOCUMENT_AI_KEY_VALUE_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError("Google Cloud project ID, location, or key-value processor ID not provided.")

    document_client_helper = DocumentClient(config)
    client = document_client_helper.get_google_document_ai_client()

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_input.document_bytes,
        mime_type=document_input.mime_type,
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    key_values = {}
    for form_field in document.form_fields:
        field_name = documentai.get_text_anchor_text(form_field.field_name.text_anchor, document.text)
        field_value = documentai.get_text_anchor_text(form_field.field_value.text_anchor, document.text)
        key_values[field_name] = field_value

    return ExtractedKeyValues(key_values=key_values)
