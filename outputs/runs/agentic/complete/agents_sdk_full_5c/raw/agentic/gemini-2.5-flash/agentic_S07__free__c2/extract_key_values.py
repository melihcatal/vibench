from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentProcessingRequest, KeyValueExtractionResponse, KeyValueParagraph

def extract_key_values(request: DocumentProcessingRequest) -> KeyValueExtractionResponse:
    """Extracts key-value pairs from a form-like document using Google Cloud Document AI.
    The Form Parser processor is specifically designed for this task.
    """
    client = get_documentai_client()

    # FORM_PARSER_PROCESSOR_V1 is ideal for key-value extraction.
    processor_id = "FORM_PARSER_PROCESSOR_V1"  
    name = client.processor_path(request.project_id, request.location, processor_id)

    document = documentai.RawDocument(content=request.file_content, mime_type=request.mime_type)

    response = client.process_document(
        name=name,
        raw_document=document
    )

    key_value_pairs = []
    for page in response.document.pages:
        for form_field in page.form_fields:
            key_text = documentai.get_text_anchor_text(form_field.field_name.text_anchor, response.document.text)
            value_text = documentai.get_text_anchor_text(form_field.field_value.text_anchor, response.document.text)
            key_value_pairs.append(KeyValueParagraph(key=key_text, value=value_text))

    return KeyValueExtractionResponse(key_value_pairs=key_value_pairs)
