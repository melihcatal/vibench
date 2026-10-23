import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

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
        processor_id (str): The ID of your Document AI processor (e.g., "YOUR_PROCESSOR_ID").
        file_path (str): The path to the document file.
        file_mime_type (str): The MIME type of the document (e.g., "application/pdf").
    """

    # Set up the Document AI client
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    raw_document = documentai.RawDocument(
        content=image_content, mime_type=file_mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    print(f"Document processing complete. Text: {document.text}\n")

    for page in document.pages:
        print(f"Page {page.page_number}:")
        if page.tables:
            for i, table in enumerate(page.tables):
                print(f"  Table {i + 1}:")
                # Iterate over rows and cells to reconstruct table structure
                # This is a simplified example; actual reconstruction can be complex
                for row_idx, body_row in enumerate(table.body_rows):
                    row_cells_text = []
                    for cell_idx, cell in enumerate(body_row.cells):
                        cell_text = documentai.get_text(cell.layout.text_anchor, document.text)
                        row_cells_text.append(f"Cell {cell_idx + 1}: '{cell_text.strip()}'")
                    print(f"    Row {row_idx + 1}: {' | '.join(row_cells_text)}")

# Example usage (replace with your actual values)
if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or configure authentication using other methods like `gcloud auth application-default login`
    # For more details: https://cloud.google.com/docs/authentication/production#auth-cloud-sdks

    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us")  # e.g., "us", "eu"
    PROCESSOR_ID = os.getenv("DOCUMENT_AI_PROCESSOR_ID", "your-processor-id") # e.g., "your-processor-id"

    # Path to your document
    DOCUMENT_FILE_PATH = "path/to/your/document.pdf"  # e.g., "path/to/invoice.pdf"
    DOCUMENT_MIME_TYPE = "application/pdf"  # e.g., "application/pdf", "image/tiff"

    # Make sure to create a processor in the Google Cloud Console for "Table Parser" or "Form Parser"
    # and enable the Document AI API.
    # Replace the placeholder values with your actual project ID, location, and processor ID.

    # This example requires a document file to be present at DOCUMENT_FILE_PATH.
    # For a full example with creating a processor, refer to Google Cloud Document AI documentation.

    print("Please replace 'your-gcp-project-id', 'your-processor-id', and 'path/to/your/document.pdf' ")
    print("with your actual values and ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set.")
    print("Example: DOCUMENT_FILE_PATH = 'invoice.pdf'")
    print("You can also set these values as environment variables: GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_LOCATION, DOCUMENT_AI_PROCESSOR_ID.")

    # Uncomment the following line to run the extraction after configuring
    # extract_tables_from_document(PROJECT_ID, LOCATION, PROCESSOR_ID, DOCUMENT_FILE_PATH, DOCUMENT_MIME_TYPE)
