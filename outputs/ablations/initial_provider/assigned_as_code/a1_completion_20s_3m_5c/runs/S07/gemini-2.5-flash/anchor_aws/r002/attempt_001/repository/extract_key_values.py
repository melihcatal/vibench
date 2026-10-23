from document_client import DocumentClient, get_project_id
from document_models import DocumentExtractionRequest, KeyValueExtractionResponse
from google.cloud import documentai_v1beta3 as documentai

def extract_key_values(request: DocumentExtractionRequest) -> KeyValueExtractionResponse:
    project_id = get_project_id()
    doc_client_helper = DocumentClient(project_id=project_id, location=request.location)
    client = doc_client_helper.get_documentai_client()

    # Use a specific processor for key-value pair extraction, e.g., 'FORM_PARSER_PROCESSOR'
    # Replace with your actual processor ID if needed
    processor_id = request.processor_id or "your-key-value-processor-id"
    name = client.processor_path(project_id, request.location, processor_id)

    raw_document = documentai.RawDocument(
        content=request.document_bytes, mime_type=request.mime_type
    )
    process_options = documentai.ProcessOptions(ocr_config=documentai.OcrConfig(enable_native_pdf_parsing=True))

    try:
        response = client.process_document(
            name=name,
            raw_document=raw_document,
            process_options=process_options
        )
        document = response.document

        key_value_pairs = []
        for entity in document.entities:
            if entity.type_ == "form_field":
                key_value_pairs.append({
                    "field_name": entity.mention_text,
                    "field_value": entity.normalized_value.text if entity.normalized_value else entity.text_anchor.content
                })

        return KeyValueExtractionResponse(key_value_pairs=key_value_pairs)

    except Exception as e:
        print(f"Error extracting key-value pairs: {e}")
        return KeyValueExtractionResponse()
