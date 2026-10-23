import os
from document_client import DocumentClient
from document_models import DocumentExtractionRequest, DocumentExtractionResponse
from google.cloud import documentai_v1 as documentai


def extract_tables(request: DocumentExtractionRequest) -> DocumentExtractionResponse:
    client_helper = DocumentClient()
    client = client_helper.get_documentai_client()
    project_id = client_helper.project_id
    location = client_helper.location
    processor_id = os.getenv(
        "DOCUMENTAI_TABLE_PROCESSOR_ID"
    )  # e.g., "YOUR_TABLE_PROCESSOR_ID"

    if not project_id or not processor_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID and DOCUMENTAI_TABLE_PROCESSOR_ID environment variables must be set."
        )

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=request.content,
        mime_type=request.mime_type,
    )

    request_obj = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request_obj)

    # Extract tables from the document object
    tables_data = []
    if result.document.pages:
        for page in result.document.pages:
            for table in page.tables:
                table_content = []
                # Simple extraction, can be more sophisticated
                for row in table.body_rows:
                    row_data = []
                    for cell in row.cells:
                        row_data.append(
                            cell.layout.text_anchor.text_segments
                        )  # This is a simplification
                    table_content.append(row_data)
                tables_data.append(table_content)

    return DocumentExtractionResponse(
        text=result.document.text, entities=tables_data, document_obj=result.document
    )
