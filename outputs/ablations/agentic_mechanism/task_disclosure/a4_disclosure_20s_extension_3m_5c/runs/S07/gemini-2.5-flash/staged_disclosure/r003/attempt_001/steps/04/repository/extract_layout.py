import os
from google.cloud import documentai_v1beta3 as documentai

def extract_layout_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    file_type: str,
):
    """
    Extracts layout information from a document using Google Cloud Document AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The location of the processor (e.g., "us").
        processor_id (str): The ID of the document processor to use.
        file_path (str): The path to the document file.
        file_type (str): The MIME type of the document (e.g., "application/pdf").
    """

    # Create a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=file_type),
    )

    result = client.process_document(request=request)

    document = result.document
    print(f"Document processing complete. Text: {document.text}\n")

    # For a full list of document object properties, please reference:
    # https://cloud.google.com/python/docs/reference/documentai/latest/google.cloud.documentai_v1beta3.types.Document

    # Extracting layout information (example: paragraphs)
    print("Paragraphs:")
    for paragraph in document.paragraphs:
        # Paragraph confidence is estimate of overall accuracy but not a reliable indicator
        # of the correctness of any single OCR segment.
        print(f"  Paragraph Text: {paragraph.layout.text_anchor.text_segments[0].start_index}")

    # You can similarly access other layout elements like lines, blocks, tokens, etc.
    # For example, to access lines:
    print("\nLines:")
    for page in document.pages:
        for line in page.lines:
            print(f"  Line Text: {line.layout.text_anchor.text_segments[0].start_index}")


if __name__ == "__main__":
    # Replace with your actual project ID, location, processor ID, and file details
    PROJECT_ID = "your-project-id"
    LOCATION = "us"  # e.g., "us"
    PROCESSOR_ID = "your-processor-id"  # Create a "FORM_PARSER_PROCESSOR" or "GENERAL_PROCESSOR" in Document AI
    FILE_PATH = "path/to/your/document.pdf"  # e.g., "document.pdf"
    FILE_TYPE = "application/pdf"  # e.g., "application/pdf" or "image/png"

    # Example usage:
    # Make sure to install the Google Cloud Document AI client library:
    # pip install google-cloud-documentai

    # You'll also need to authenticate. For local development, you can use:
    # gcloud auth application-default login

    # extract_layout_from_document(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH, FILE_TYPE)
