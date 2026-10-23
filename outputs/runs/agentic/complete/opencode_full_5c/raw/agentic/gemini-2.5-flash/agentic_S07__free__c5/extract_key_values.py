import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentKeyValueExtractionResponse


def extract_key_values_from_document(
    file_content: bytes, mime_type: str
) -> DocumentKeyValueExtractionResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")  # e.g., "us"
    processor_id = os.environ.get(
        "GOOGLE_CLOUD_DOCUMENTAI_PROCESSOR_ID_KEY_VALUES", "FORM_PROCESSOR_ID_HERE"
    )  # Replace with your Form Parser processor ID

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = get_documentai_client()

    resource_name = client.processor_path(project_id, location, processor_id)

    document = documentai.RawDocument(content=file_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=document)

    result = client.process_document(request=request)
    document_response = result.document

    key_value_pairs = {}
    for entity in document_response.entities:
        if entity.type_ == "form_field" and entity.properties:
            for prop in entity.properties:
                key = documentai.get_text_anchor_text(
                    entity.text_anchor, document_response.text
                )
                value = documentai.get_text_anchor_text(
                    prop.text_anchor, document_response.text
                )
                key_value_pairs[key] = value

    return DocumentKeyValueExtractionResponse(key_value_pairs=key_value_pairs)
