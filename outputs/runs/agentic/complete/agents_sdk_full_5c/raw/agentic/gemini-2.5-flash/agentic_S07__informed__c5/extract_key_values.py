import os
from google.cloud import documentai_v1beta3 as documentai
from document_client import get_documentai_client
from document_models import DocumentProcessingRequest, DocumentKeyValueExtractionResponse

def extract_key_values(request: DocumentProcessingRequest) -> DocumentKeyValueExtractionResponse:
    """Extracts key-value pairs from a form-like document using Google Document AI."""
    client = get_documentai_client()
    processor_name = client.processor_path(
        os.environ.get("GOOGLE_CLOUD_PROJECT"),
        os.environ.get("GOOGLE_CLOUD_LOCATION"),
        os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID_GENERAL") # Use a general processor
    )

    with open(request.document_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type=request.mime_type
    )

    request_docai = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document
    )

    result = client.process_document(request_docai)
    document = result.document

    key_value_pairs = {}
    for page in document.pages:
        for form_field in page.form_fields:
            # Assuming field_name is the key and corrected_value is the value
            # You might need to adjust this based on the specific processor and document type
            field_name = document.text[int(form_field.field_name.text_anchor.text_segments[0].start_index):int(form_field.field_name.text_anchor.text_segments[0].end_index)]
            field_value = document.text[int(form_field.field_value.text_anchor.text_segments[0].start_index):int(form_field.field_value.text_anchor.text_segments[0].end_index)]
            key_value_pairs[field_name] = field_value

    return DocumentKeyValueExtractionResponse(
        key_value_pairs=key_value_pairs
    )
