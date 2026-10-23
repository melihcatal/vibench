from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os
from typing import List, Dict, Any

def extract_tables(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> List[Dict[str, Any]]:
    """Extracts table cells and row structure from a document using Google Document AI."""

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_tables = []

    for page in document.pages:
        for table in page.tables:
            table_data = {
                "page_number": page.page_number,
                "num_rows": table.num_rows,
                "num_columns": table.num_columns,
                "header_rows": [],
                "body_rows": [],
            }

            # Extract header rows
            for header_row in table.header_rows:
                row_cells = []
                for cell in header_row.cells:
                    row_cells.append(cell.layout.text_anchor.text_content if cell.layout.text_anchor.text_segments else "")
                table_data["header_rows"].append(row_cells)
            
            # Extract body rows
            for body_row in table.body_rows:
                row_cells = []
                for cell in body_row.cells:
                    row_cells.append(cell.layout.text_anchor.text_content if cell.layout.text_anchor.text_segments else "")
                table_data["body_rows"].append(row_cells)
            
            extracted_tables.append(table_data)
    
    return extracted_tables

if __name__ == '__main__':
    # Placeholder for actual usage, replace with your project details and a dummy file
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # Use a general processor like "form-parser" or a custom processor trained for tables.
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = "us" # e.g., "us"
    processor_id = os.getenv("DOCUMENTAI_TABLE_PROCESSOR_ID", "your-table-processor-id") # e.g., "form-parser"
    
    # Create a dummy image file for testing
    dummy_file_path = "dummy.png"
    with open(dummy_file_path, "wb") as f:
        f.write(b"dummy image content") # Replace with actual image content for real testing

    try:
        # result_tables = extract_tables(project_id, location, processor_id, dummy_file_path, "image/png")
        # print(f"Extracted Tables: {result_tables}")
        print("Run with actual Document AI credentials and a valid processor ID and image file.")
    except Exception as e:
        print(f"Error extracting tables: {e}")
    finally:
        os.remove(dummy_file_path)
