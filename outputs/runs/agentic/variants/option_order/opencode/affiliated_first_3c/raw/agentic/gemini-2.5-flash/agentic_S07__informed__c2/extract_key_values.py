from google.cloud import documentai_v1beta3 as documentai
from document_client import get_documentai_client
from document_models import DocumentRequest, KeyValueExtractionResponse


def extract_key_values(request: DocumentRequest) -> KeyValueExtractionResponse:
    client = get_documentai_client()
    processor_name = client.processor_path(
        request.project_id, request.location, request.processor_id
    )

    raw_document = documentai.RawDocument(
        content=request.file_content,
        mime_type=request.mime_type,
    )
    request_options = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request_options)

    key_values = {}
    for entity in result.document.entities:
        if entity.type_ == "form_field":  # Assuming form fields are key-value pairs
            key = client.get_text(result.document.text, entity.text_anchor)
            value = ""
            if (
                entity.page_anchor and entity.page_anchor.page_refs
            ):  # Check for value in page_refs
                for page_ref in entity.page_anchor.page_refs:
                    value = client.get_text(
                        result.document.text, page_ref.layout.text_anchor
                    )  # Get text from the page_ref layout
            elif (
                entity.properties
            ):  # Check for value in properties if not found in page_refs
                for prop in entity.properties:
                    value = client.get_text(result.document.text, prop.text_anchor)
                    break
            key_values[key.strip()] = value.strip()

    return KeyValueExtractionResponse(key_values=key_values)
