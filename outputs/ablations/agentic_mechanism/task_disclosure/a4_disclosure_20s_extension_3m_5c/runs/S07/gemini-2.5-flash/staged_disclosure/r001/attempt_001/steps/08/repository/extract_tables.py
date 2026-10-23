from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os

def extract_tables_from_document(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts table cells and row structure from a document using Google Cloud Document AI.
    """
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf" # Or other appropriate mime type like "image/jpeg"
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    extracted_tables = []
    for table_idx, table in enumerate(document.tables):
        current_table = {"table_index": table_idx, "header_rows": [], "body_rows": []}

        # Extract header rows
        for row_idx, row in enumerate(table.header_rows):
            header_row_cells = []
            for cell_idx, cell in enumerate(row.cells):
                cell_text = document.text[cell.layout.text_anchor.text_segments[0].start_index:cell.layout.text_anchor.text_segments[0].end_index]
                header_row_cells.append({"cell_index": cell_idx, "text": cell_text.strip()})
            current_table["header_rows"].append({"row_index": row_idx, "cells": header_row_cells})

        # Extract body rows
        for row_idx, row in enumerate(table.body_rows):
            body_row_cells = []
            for cell_idx, cell in enumerate(row.cells):
                cell_text = document.text[cell.layout.text_anchor.text_segments[0].start_index:cell.layout.text_anchor.text_segments[0].end_index]
                body_row_cells.append({"cell_index": cell_idx, "text": cell_text.strip()})
            current_table["body_rows"].append({"row_index": row_idx, "cells": body_row_cells})

        extracted_tables.append(current_table)

    return extracted_tables

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID, location, and processor ID
    # For example:
    # PROJECT_ID = "your-gcp-project-id"
    # LOCATION = "us"  # e.g., "us" or "eu"
    # PROCESSOR_ID = "your-processor-id" # Create a "Table Parser" processor in Document AI

    # Replace with the path to your document file (e.g., PDF or image)
    # FILE_PATH = "path/to/your/document.pdf"

    # Example usage (commented out as per instructions not to include example usage,
    # but provides structure for how a user might call it)
    #
    # extracted_data = extract_tables_from_document(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
    # if extracted_data:
    #     print("Tables extracted successfully:")
    #     for table in extracted_data:
    #         print(f"Table {table['table_index']}:")
    #         print("  Header Rows:")
    #         for h_row in table['header_rows']:
    #             print(f"    Row {h_row['row_index']}: {[cell['text'] for cell in h_row['cells']]}")
    #         print("  Body Rows:")
    #         for b_row in table['body_rows']:
    #             print(f"    Row {b_row['row_index']}: {[cell['text'] for cell in b_row['cells']]}")
    # else:
    #     print("No tables extracted or an error occurred.")
    pass
