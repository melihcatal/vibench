import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_path

def extract_plain_text(project_id: str, location: str, processor_id: str, file_path: str) -> str:
    """Extracts plain text from a document using Google Document AI."""
    client = get_documentai_client()
    processor_path = get_processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=processor_path, raw_document=document)

    response = client.process_document(request=request)
    return response.document.text

if __name__ == '__main__':
    # This is placeholder for demonstration. In a real application,
    # these would come from environment variables or a config file.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    LOCATION = "us"  # e.g., "us" or "eu"
    PROCESSOR_ID = os.getenv("DOCUMENTAI_PROCESSOR_ID", "your-general-processor-id") # e.g., "ocr-v1" or "pretrained-form-parser"
    SAMPLE_FILE = "path/to/your/document.pdf" # Replace with a path to a real document

    # Make sure to set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or authenticate otherwise.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"

    # print(f"Extracted Text: {extract_plain_text(PROJECT_ID, LOCATION, PROCESSOR_ID, SAMPLE_FILE)}")
