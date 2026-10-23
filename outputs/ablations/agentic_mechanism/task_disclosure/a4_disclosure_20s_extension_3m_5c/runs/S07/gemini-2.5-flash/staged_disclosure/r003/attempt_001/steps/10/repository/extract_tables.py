import os
from google.cloud import documentai_v1 as documentai

def extract_tables_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    file_mime_type: str,
):
    """
    Extracts table cells and row structure from a document using Google Cloud Document AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region (e.g., "us").
        processor_id (str): The ID of the Document AI processor.
        file_path (str): The path to the document file.
        file_mime_type (str): The MIME type of the document (e.g., "application/pdf").

    Returns:
        documentai.Document: The processed document object containing table information.
    """

    # Create a client
    client = documentai.DocumentProcessorServiceClient()

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
            content=image_content, mime_type=file_mime_type
        ),
    )

    result = client.process_document(request=request)

    return result.document

if __name__ == "__main__":
    # This is an example of how to use the function.
    # Replace with your actual project ID, location, processor ID, and file details.
    PROJECT_ID = "your-project-id"  # Replace with your Google Cloud Project ID
    LOCATION = "us"  # Replace with your Document AI processor location
    PROCESSOR_ID = "your-processor-id"  # Replace with your Document AI processor ID
    FILE_PATH = "path/to/your/document.pdf"  # Replace with the path to your document
    FILE_MIME_TYPE = "application/pdf"  # Replace with the MIME type of your document

    print(f"Extracting tables from {FILE_PATH} using Document AI...")

    try:
        document = extract_tables_from_document(
            PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH, FILE_MIME_TYPE
        )

        print("Document processing complete.")

        if document.pages:
            for i, page in enumerate(document.pages):
                print(f"--- Page {i + 1} ---")
                for table_num, table in enumerate(page.tables):
                    print(f"  Table {table_num + 1}:")
                    for row_num, row in enumerate(table.header_rows):
                        row_text = "|".join([cell.layout.text_anchor.content for cell in row.cells])
                        print(f"    Header Row {row_num + 1}: {row_text}")
                    for row_num, row in enumerate(table.body_rows):
                        row_text = "|".join([cell.layout.text_anchor.content for cell in row.cells])
                        print(f"    Body Row {row_num + 1}: {row_text}")
        else:
            print("No pages found in the document.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have:")
        print("1. Replaced 'your-project-id', 'your-processor-id', and 'path/to/your/document.pdf' with actual values.")
        print("2. Enabled the Document AI API in your Google Cloud project.")
        print("3. Created a Document AI processor (e.g., a 'General Processor') and noted its ID.")
        print("4. Authenticated your environment (e.g., using `gcloud auth application-default login`).")
