from document_client import DocumentClient, get_project_id
from document_models import DocumentExtractionRequest, TableExtractionResponse
from google.cloud import documentai_v1beta3 as documentai

def extract_tables(request: DocumentExtractionRequest) -> TableExtractionResponse:
    project_id = get_project_id()
    doc_client_helper = DocumentClient(project_id=project_id, location=request.location)
    client = doc_client_helper.get_documentai_client()

    # Use a specific processor for table extraction, e.g., 'FORM_PARSER_PROCESSOR'
    # Replace with your actual processor ID if needed
    processor_id = request.processor_id or "your-table-processor-id"
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

        tables_data = []
        for page in document.pages:
            for table in page.tables:
                rows_data = []
                for row in table.body_rows:
                    cells_data = []
                    for cell in row.cells:
                        cells_data.append({"text": cell.text_anchor.content})
                    rows_data.append({"cells": cells_data})
                tables_data.append({"rows": rows_data})

        return TableExtractionResponse(tables=tables_data)

    except Exception as e:
        print(f"Error extracting tables: {e}")
        return TableExtractionResponse()
