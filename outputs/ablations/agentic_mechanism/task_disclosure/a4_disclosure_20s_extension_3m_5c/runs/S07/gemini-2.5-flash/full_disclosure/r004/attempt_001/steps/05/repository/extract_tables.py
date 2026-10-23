from google.cloud import documentai_v1 as documentai

def extract_tables_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> dict:
    """
    Extracts table cells and row structure from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of the table parser processor.
        file_path: The path to the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        A dictionary containing the extracted table data.
    """
    documentai_client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Document AI Document
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = documentai_client.process_document(request=request)
    document = result.document

    tables_data = []
    if document.pages:
        for page in document.pages:
            for table_index, table in enumerate(page.tables):
                table_info = {
                    "page": page.page_number,
                    "table_index": table_index,
                    "header_rows": [],
                    "body_rows": [],
                }
                # Extract header rows
                for row_index, row in enumerate(table.header_rows):
                    cells = []
                    for cell in row.cells:
                        cells.append({
                            "text": documentai.Document.to_html_string(cell.layout.text_anchor, document.text),
                            "row_span": cell.row_span,
                            "col_span": cell.col_span,
                        })
                    table_info["header_rows"].append({"row_index": row_index, "cells": cells})

                # Extract body rows
                for row_index, row in enumerate(table.body_rows):
                    cells = []
                    for cell in row.cells:
                        cells.append({
                            "text": documentai.Document.to_html_string(cell.layout.text_anchor, document.text),
                            "row_span": cell.row_span,
                            "col_span": cell.col_span,
                        })
                    table_info["body_rows"].append({"row_index": row_index, "cells": cells})
                tables_data.append(table_info)

    return {"tables": tables_data, "text": document.text}
