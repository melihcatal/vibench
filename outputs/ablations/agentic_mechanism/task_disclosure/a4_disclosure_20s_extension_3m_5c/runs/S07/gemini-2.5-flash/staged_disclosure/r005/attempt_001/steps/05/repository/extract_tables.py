import os
from google.cloud import documentai_v1beta3 as documentai

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
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region to run the processor in (e.g., "us").
        processor_id (str): The ID of the table parser processor.
        file_path (str): The path to the document file.
        mime_type (str): The MIME type of the document (e.g., "application/pdf").

    Returns:
        dict: A dictionary containing the extracted table data.
    """

    documentai_client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = documentai_client.process_document(request=request)
    document = result.document

    tables_data = []
    for page in document.pages:
        for table_num, table in enumerate(page.tables):
            table_info = {"page": page.page_number, "table_num": table_num + 1, "rows": []}
            for row in table.body_rows:
                row_data = []
                for cell in row.cells:
                    cell_text = documentai.text_anchor_to_text(cell.layout.text_anchor, document.text)
                    row_data.append(cell_text.strip())
                table_info["rows"].append(row_data)
            tables_data.append(table_info)

    return {"tables": tables_data}

if __name__ == "__main__":
    # Example Usage (replace with your actual values)
    # project_id = "YOUR_PROJECT_ID"
    # location = "YOUR_LOCATION"  # e.g., "us"
    # processor_id = "YOUR_PROCESSOR_ID"  # e.g., "YOUR_TABLE_PARSER_PROCESSOR_ID"
    # file_path = "path/to/your/document.pdf"
    # mime_type = "application/pdf"

    # print("Remember to enable the Document AI API and set up authentication.")
    # print("Refer to Google Cloud Document AI documentation for detailed setup.")

    # extracted_data = extract_tables_from_document(
    #     project_id, location, processor_id, file_path, mime_type
    # )
    # print(extracted_data)
    pass
