import os
from document_client import DocumentClient
from document_models import DocumentExtractionRequest, DocumentExtractionResponse
from google.cloud import documentai_v1 as documentai


def extract_key_value_pairs(
    request: DocumentExtractionRequest,
) -> DocumentExtractionResponse:
    client_helper = DocumentClient()
    client = client_helper.get_documentai_client()
    project_id = client_helper.project_id
    location = client_helper.location
    processor_id = os.getenv(
        "DOCUMENTAI_KEY_VALUE_PROCESSOR_ID"
    )  # e.g., "YOUR_KEY_VALUE_PROCESSOR_ID"

    if not project_id or not processor_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID and DOCUMENTAI_KEY_VALUE_PROCESSOR_ID environment variables must be set."
        )

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=request.content,
        mime_type=request.mime_type,
    )

    request_obj = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request_obj)

    key_value_pairs = {}
    if result.document.entities:
        for entity in result.document.entities:
            if (
                entity.type_ == "form_field"
            ):  # This is a common type for key-value pairs
                key = entity.mention_text
                value = (
                    entity.normalized_value.text
                    if entity.normalized_value
                    else entity.text_anchor.text_segments
                )
                key_value_pairs[key] = value

    return DocumentExtractionResponse(
        text=result.document.text,
        entities=key_value_pairs,
        document_obj=result.document,
    )
