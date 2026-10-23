from document_client import DocumentClient, get_project_id
from document_models import FieldExtractionRequest, FieldExtractionResponse
from google.cloud import documentai_v1beta3 as documentai

def document_field_extraction(request: FieldExtractionRequest) -> FieldExtractionResponse:
    project_id = get_project_id()
    doc_client_helper = DocumentClient(project_id=project_id, location=request.location)
    client = doc_client_helper.get_documentai_client()

    # Use a specific processor for structured field extraction (e.g., a custom processor)
    # Replace with your actual processor ID if needed
    processor_id = request.processor_id or "your-field-extraction-processor-id"
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

        extracted_fields = {}
        for entity in document.entities:
            # Assuming entities are the structured fields we want to extract
            field_value = entity.normalized_value.text if entity.normalized_value else entity.text_anchor.content
            extracted_fields[entity.type_] = field_value

        return FieldExtractionResponse(fields=extracted_fields)

    except Exception as e:
        print(f"Error extracting fields: {e}")
        return FieldExtractionResponse()
