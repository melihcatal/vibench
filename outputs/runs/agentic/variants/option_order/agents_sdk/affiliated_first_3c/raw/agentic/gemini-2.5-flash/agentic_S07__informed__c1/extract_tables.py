import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_path

def extract_tables(project_id: str, location: str, processor_id: str, file_path: str):
    """Extracts tables from a document using Google Document AI."""
    client = get_documentai_client()
    processor_path = get_processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=processor_path, raw_document=document)

    response = client.process_document(request=request)
    doc = response.document

    extracted_tables = []

    for page in doc.pages:
        for table in page.tables:
            table_data = {
                "page_number": page.page_number,
                "num_rows": table.num_rows,
                "num_cols": table.num_cols,
                "header_rows": [],
                "body_rows": []
            }

            # Extract header rows
            for row in table.header_rows:
                header_cells = []
                for cell in row.cells:
                    header_cells.append(doc.text[cell.layout.text_anchor.text_segments[0].start_index:cell.layout.text_anchor.text_segments[0].end_index])
                table_data["header_rows"].append(header_cells)

            # Extract body rows
            for row in table.body_rows:
                body_cells = []
                for cell in row.cells:
                    body_cells.append(doc.text[cell.layout.text_anchor.text_segments[0].start_index:cell.layout.text_anchor.text_segments[0].end_index])
                table_data["body_rows"].append(body_cells)
            extracted_tables.append(table_data)

    return extracted_tables

if __name__ == '__main__':
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    LOCATION = "us"
    PROCESSOR_ID = os.getenv("DOCUMENTAI_PROCESSOR_ID", "your-general-processor-id") # e.g., "form-parser-v2.0-2022-09-18"
    SAMPLE_FILE = "path/to/your/document.pdf"

    # tables = extract_tables(PROJECT_ID, LOCATION, PROCESSOR_ID, SAMPLE_FILE)
    # for table in tables:
    #     print(f"Table on Page {table['page_number']}:")
    #     print("Headers:", table['header_rows'])
    #     print("Body:", table['body_rows'])
