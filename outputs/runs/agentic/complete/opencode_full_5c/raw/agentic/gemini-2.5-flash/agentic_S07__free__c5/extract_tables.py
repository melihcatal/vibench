import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentTableExtractionResponse


def extract_tables_from_document(
    file_content: bytes, mime_type: str
) -> DocumentTableExtractionResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")  # e.g., "us"
    processor_id = os.environ.get(
        "GOOGLE_CLOUD_DOCUMENTAI_PROCESSOR_ID_TABLES", "TABLE_PROCESSOR_ID_HERE"
    )  # Replace with your Table Parser processor ID

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = get_documentai_client()

    resource_name = client.processor_path(project_id, location, processor_id)

    document = documentai.RawDocument(content=file_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=document)

    result = client.process_document(request=request)
    document_response = result.document

    extracted_tables = []
    for page in document_response.pages:
        for table in page.tables:
            table_data = {
                "num_rows": table.num_rows,
                "num_columns": table.num_columns,
                "header_rows": [],
                "body_rows": [],
            }
            # Extract header rows
            for row in table.header_rows:
                row_cells = []
                for cell in row.cells:
                    row_cells.append(
                        documentai.get_text_anchor_text(
                            cell.layout.text_anchor, document_response.text
                        )
                    )
                table_data["header_rows"].append(row_cells)

            # Extract body rows
            for row in table.body_rows:
                row_cells = []
                for cell in row.cells:
                    row_cells.append(
                        documentai.get_text_anchor_text(
                            cell.layout.text_anchor, document_response.text
                        )
                    )
                table_data["body_rows"].append(row_cells)

            extracted_tables.append(table_data)

    return DocumentTableExtractionResponse(tables=extracted_tables)
