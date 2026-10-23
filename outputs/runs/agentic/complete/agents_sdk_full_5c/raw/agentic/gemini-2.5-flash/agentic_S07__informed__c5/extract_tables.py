import os
from google.cloud import documentai_v1beta3 as documentai
from document_client import get_documentai_client
from document_models import DocumentProcessingRequest, DocumentTableExtractionResponse

def extract_tables(request: DocumentProcessingRequest) -> DocumentTableExtractionResponse:
    """Extracts table cells and row structure from a document using Google Document AI."""
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

    extracted_tables = []
    for page in document.pages:
        for table in page.tables:
            table_data = {
                "num_rows": table.num_rows,
                "num_columns": table.num_columns,
                "header_rows": [],
                "body_rows": []
            }
            for row in table.header_rows:
                row_cells = []
                for cell in row.cells:
                    row_cells.append(document.text[int(cell.layout.text_anchor.text_segments[0].start_index):int(cell.layout.text_anchor.text_segments[0].end_index)])
                table_data["header_rows"].append(row_cells)
            for row in table.body_rows:
                row_cells = []
                for cell in row.cells:
                    row_cells.append(document.text[int(cell.layout.text_anchor.text_segments[0].start_index):int(cell.layout.text_anchor.text_segments[0].end_index)])
                table_data["body_rows"].append(row_cells)
            extracted_tables.append(table_data)

    return DocumentTableExtractionResponse(
        tables=extracted_tables
    )
