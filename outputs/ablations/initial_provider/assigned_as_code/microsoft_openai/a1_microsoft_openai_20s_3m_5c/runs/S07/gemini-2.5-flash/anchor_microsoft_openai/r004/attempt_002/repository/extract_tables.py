import os
from google.cloud import documentai_v1 as documentai
from document_client import DocumentClient
from document_models import DocumentInput, ExtractedTables

def extract_tables(document_input: DocumentInput, config: dict = None) -> ExtractedTables:
    config = config or {}
    project_id = config.get("GOOGLE_CLOUD_PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = config.get("GOOGLE_CLOUD_LOCATION") or os.environ.get("GOOGLE_CLOUD_LOCATION", "us") # e.g., "us"
    processor_id = config.get("GOOGLE_CLOUD_DOCUMENT_AI_TABLE_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError("Google Cloud project ID, location, or table processor ID not provided.")

    document_client_helper = DocumentClient(config)
    client = document_client_helper.get_google_document_ai_client()

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_input.document_bytes,
        mime_type=document_input.mime_type,
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    all_tables = []
    for page in document.pages:
        for table in page.tables:
            table_data = {
                "page_number": page.page_number,
                "num_rows": table.header_rows[0].cells[0].row_span.end if table.header_rows else len(table.body_rows),
                "num_cols": table.header_rows[0].cells[0].col_span.end if table.header_rows else max([cell.col_span.end for row in table.body_rows for cell in row.cells]) if table.body_rows else 0,
                "header_rows": [],
                "body_rows": []
            }

            for header_row in table.header_rows:
                row_cells = []
                for cell in header_row.cells:
                    row_cells.append({"text": documentai.get_text_anchor_text(cell.layout.text_anchor, document.text)})
                table_data["header_rows"].append(row_cells)
            
            for body_row in table.body_rows:
                row_cells = []
                for cell in body_row.cells:
                    row_cells.append({"text": documentai.get_text_anchor_text(cell.layout.text_anchor, document.text)})
                table_data["body_rows"].append(row_cells)

            all_tables.append(table_data)

    return ExtractedTables(tables=all_tables)
