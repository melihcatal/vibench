import os
from google.cloud import documentai_v1 as documentai

def extract_tables_from_document(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts table cells and row structure from a document using Google Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf",
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    extracted_tables = []

    for page in document.pages:
        for table in page.tables:
            table_data = {
                "page_number": page.page_number,
                "rows": []
            }
            # Extract header rows
            for header_row in table.header_rows:
                row_cells = []
                for cell in header_row.cells:
                    cell_text = documentai.Document.Page.Layout.text_anchor_to_text(cell.layout.text_anchor, document.text)
                    row_cells.append(cell_text)
                table_data["rows"].append({"type": "header", "cells": row_cells})

            # Extract body rows
            for body_row in table.body_rows:
                row_cells = []
                for cell in body_row.cells:
                    cell_text = documentai.Document.Page.Layout.text_anchor_to_text(cell.layout.text_anchor, document.text)
                    row_cells.append(cell_text)
                table_data["rows"].append({"type": "body", "cells": row_cells})
            
            extracted_tables.append(table_data)

    return extracted_tables

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID_TABLE") # Often a FORM_PARSER or a specialized table processor
    file_to_process = "path/to/your/document_with_tables.pdf"

    if project_id and processor_id and os.path.exists(file_to_process):
        tables_data = extract_tables_from_document(project_id, location, processor_id, file_to_process)
        print("Extracted Tables Info:")
        import json
        print(json.dumps(tables_data, indent=2))
    else:
        print("Please set GOOGLE_CLOUD_PROJECT, DOCUMENT_AI_PROCESSOR_ID_TABLE environment variables and ensure document file exists.")
