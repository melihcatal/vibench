import os
from document_client import get_documentai_client
from document_models import DocumentContent, TableExtractionResult
from google.cloud import documentai_v1 as documentai


def extract_tables(
    doc_content: DocumentContent, project_id: str, location: str, processor_id: str
) -> TableExtractionResult:
    client = get_documentai_client()

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=doc_content.content, mime_type=doc_content.mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    tables_data = []
    for page in result.document.pages:
        for table in page.tables:
            table_cells = []
            for row_idx, row in enumerate(table.header_rows):
                row_cells = []
                for cell_idx, cell in enumerate(row.cells):
                    cell_text = client.decode_text(
                        cell.layout.text_anchor, result.document.text
                    )
                    row_cells.append(
                        {
                            "text": cell_text,
                            "row_span": cell.row_span,
                            "col_span": cell.col_span,
                            "is_header": True,
                        }
                    )
                table_cells.append(row_cells)
            for row_idx, row in enumerate(table.body_rows):
                row_cells = []
                for cell_idx, cell in enumerate(row.cells):
                    cell_text = client.decode_text(
                        cell.layout.text_anchor, result.document.text
                    )
                    row_cells.append(
                        {
                            "text": cell_text,
                            "row_span": cell.row_span,
                            "col_span": cell.col_span,
                            "is_header": False,
                        }
                    )
                table_cells.append(row_cells)
            tables_data.append({"page_number": page.page_number, "cells": table_cells})

    return TableExtractionResult(tables=tables_data)


if __name__ == "main":
    # Example Usage (replace with actual values and file content)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    LOCATION = "us"
    PROCESSOR_ID = os.environ.get(
        "GOOGLE_DOCUMENT_AI_TABLE_PROCESSOR_ID"
    )  # Use a specific table processor or general form processor

    if not all([PROJECT_ID, LOCATION, PROCESSOR_ID]):
        print(
            "Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_DOCUMENT_AI_TABLE_PROCESSOR_ID environment variables."
        )
    else:
        with open(
            "path/to/your/document.pdf", "rb"
        ) as image:  # Replace with your document path
            content = image.read()
        doc = DocumentContent(content=content, mime_type="application/pdf")
        table_result = extract_tables(doc, PROJECT_ID, LOCATION, PROCESSOR_ID)
        print("Extracted Tables:", table_result.tables)
