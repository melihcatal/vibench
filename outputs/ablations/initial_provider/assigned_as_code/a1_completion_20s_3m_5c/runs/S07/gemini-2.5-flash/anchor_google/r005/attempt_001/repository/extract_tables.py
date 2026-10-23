from google.cloud import documentai
from document_client import get_documentai_client

def extract_tables(payload, config=None):
    config = config or {}
    client = get_documentai_client(config['location'])
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"])})
    
    tables_data = []
    for page in response.document.pages:
        for table in page.tables:
            table_cells = []
            for row in table.body_rows:
                row_cells = []
                for cell in row.cells:
                    # Extract text content for each cell
                    cell_text = response.document.text[cell.layout.text_anchor.text_segments[0].start_index:cell.layout.text_anchor.text_segments[0].end_index]
                    row_cells.append(cell_text)
                table_cells.append(row_cells)
            tables_data.append({"page_number": page.page_number, "cells": table_cells})

    return {"tables": tables_data, "full_text": response.document.text}
