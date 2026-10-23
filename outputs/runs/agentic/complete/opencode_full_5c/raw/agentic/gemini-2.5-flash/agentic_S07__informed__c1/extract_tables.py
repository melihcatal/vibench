from google.cloud import documentai_v1b3 as documentai
import os


def extract_tables(project_id: str, location: str, processor_id: str, file_path: str):
    """Extracts table cells and row structure from a document using Google Document AI."""
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    tables_data = []
    for page in document.pages:
        for table_num, table in enumerate(page.tables):
            table_info = {
                "page_number": page.page_number,
                "table_number": table_num,
                "header_rows": [],
                "body_rows": [],
            }
            for row_num, header_row in enumerate(table.header_rows):
                row_cells = []
                for cell in header_row.cells:
                    row_cells.append(
                        document.text[
                            cell.layout.text_anchor.text_segments[
                                0
                            ].start_index : cell.layout.text_anchor.text_segments[
                                0
                            ].end_index
                        ]
                    )
                table_info["header_rows"].append(row_cells)
            for row_num, body_row in enumerate(table.body_rows):
                row_cells = []
                for cell in body_row.cells:
                    row_cells.append(
                        document.text[
                            cell.layout.text_anchor.text_segments[
                                0
                            ].start_index : cell.layout.text_anchor.text_segments[
                                0
                            ].end_index
                        ]
                    )
                table_info["body_rows"].append(row_cells)
            tables_data.append(table_info)
    return tables_data


if __name__ == "__main__":
    # Example usage (replace with your actual values)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us"  # e.g., "us"
    PROCESSOR_ID = (
        "YOUR_PROCESSOR_ID"  # Create a "Form Parser" or "Table Parser" in Document AI
    )
    FILE_PATH = "path/to/your/document_with_tables.pdf"

    if PROJECT_ID and PROCESSOR_ID and os.path.exists(FILE_PATH):
        extracted_tables = extract_tables(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
        print("Extracted Tables:\n", extracted_tables)
    else:
        print(
            "Please set GOOGLE_CLOUD_PROJECT, PROCESSOR_ID, and provide a valid FILE_PATH."
        )
