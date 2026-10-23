import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client


def extract_tables_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
):
    """Extracts table cells and row structure from a document using Google Document AI."""
    client = get_documentai_client()
    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    tables_data = []
    for page in document.pages:
        for table in page.tables:
            table_info = {
                "num_rows": table.num_rows,
                "num_columns": table.num_columns,
                "header_rows": [],
                "body_rows": [],
            }
            for row in table.header_rows:
                header_cells = []
                for cell in row.cells:
                    header_cells.append(
                        documentai.text_anchor_to_text(
                            cell.layout.text_anchor, document.text
                        )
                    )
                table_info["header_rows"].append(header_cells)
            for row in table.body_rows:
                body_cells = []
                for cell in row.cells:
                    body_cells.append(
                        documentai.text_anchor_to_text(
                            cell.layout.text_anchor, document.text
                        )
                    )
                table_info["body_rows"].append(body_cells)
            tables_data.append(table_info)
    return tables_data
