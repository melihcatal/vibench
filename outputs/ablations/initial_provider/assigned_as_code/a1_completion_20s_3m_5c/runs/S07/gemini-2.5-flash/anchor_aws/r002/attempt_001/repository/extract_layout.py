from document_client import DocumentClient, get_project_id
from document_models import DocumentExtractionRequest, LayoutExtractionResponse
from google.cloud import documentai_v1beta3 as documentai

def extract_layout(request: DocumentExtractionRequest) -> LayoutExtractionResponse:
    project_id = get_project_id()
    doc_client_helper = DocumentClient(project_id=project_id, location=request.location)
    client = doc_client_helper.get_documentai_client()

    # Use a specific processor for layout analysis, e.g., 'OCR_PROCESSOR' or 'FORM_PARSER_PROCESSOR'
    # Replace with your actual processor ID if needed
    processor_id = request.processor_id or "your-layout-processor-id"
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

        pages_data = []
        for page in document.pages:
            page_blocks = []
            for block in page.layout.text_segments:
                page_blocks.append({"text_segment": {"start_index": block.start_index, "end_index": block.end_index}})
            pages_data.append({"page_number": page.page_number, "blocks": page_blocks})

        return LayoutExtractionResponse(pages=pages_data)

    except Exception as e:
        print(f"Error extracting layout: {e}")
        return LayoutExtractionResponse()
