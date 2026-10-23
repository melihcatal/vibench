
from google.cloud import documentai_v1 as documentai

def extract_tables_from_document(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts table cells and row structure from a document using Google Cloud Document AI.
    """

    # You can set the api_endpoint if your processor is not in the default region.
    # For example, "us-documentai.googleapis.com" if your processor is in the US.
    client = documentai.DocumentProcessorServiceClient()

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

    # Configure the process request
    name = client.processor_path(project_id, location, processor_id)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    tables_data = []
    for page in document.pages:
        for table_idx, table in enumerate(page.tables):
            table_info = {
                "page_number": page.page_number,
                "header_rows": [],
                "body_rows": []
            }

            # Extract header rows
            for row in table.header_rows:
                header_row_data = []
                for cell in row.cells:
                    header_row_data.append(cell.layout.text_anchor.text_segments[0].text_content if cell.layout.text_anchor.text_segments else "")
                table_info["header_rows"].append(header_row_data)

            # Extract body rows
            for row in table.body_rows:
                body_row_data = []
                for cell in row.cells:
                    body_row_data.append(cell.layout.text_anchor.text_segments[0].text_content if cell.layout.text_anchor.text_segments else "")
                table_info["body_rows"].append(body_row_data)
            tables_data.append(table_info)

    return tables_data

if __name__ == "__main__":
    # This is an example of how to use the function.
    # Replace with your actual project_id, location, processor_id, and file_path
    PROJECT_ID = "YOUR_PROJECT_ID"
    LOCATION = "YOUR_LOCATION"  # e.g., "us"
    PROCESSOR_ID = "YOUR_PROCESSOR_ID" # e.g., "YOUR_PROCESSOR_ID" for a "Table Parser" processor
    FILE_PATH = "path/to/your/document.pdf"

    # Example usage (uncomment and fill in details to run):
    # try:
    #     extracted_tables = extract_tables_from_document(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
    #     for i, table in enumerate(extracted_tables):
    #         print(f"Table {i+1} on page {table['page_number']}:")
    #         print("Header Rows:", table["header_rows"])
    #         print("Body Rows:", table["body_rows"])
    # except Exception as e:
    #     print(f"An error occurred: {e}")
