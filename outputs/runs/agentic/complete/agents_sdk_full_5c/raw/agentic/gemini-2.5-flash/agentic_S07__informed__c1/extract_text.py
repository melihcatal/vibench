from google.cloud import documentai_v1 as documentai
import os

def extract_plain_text(project_id: str, location: str, processor_id: str, file_path: str):
    """Extracts plain text from a document using Google Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    return document.text

if __name__ == '__main__':
    # These environment variables would typically be set in a production environment
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    # PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # LOCATION = "us" # e.g., "us"
    # PROCESSOR_ID = "YOUR_OCR_PROCESSOR_ID" # e.g., "YOUR_OCR_PROCESSOR_ID"

    # Placeholder values for demonstration
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "us"
    PROCESSOR_ID = "your-ocr-processor-id" # Use a generic OCR processor
    FILE_PATH = "path/to/your/document.pdf"

    # print(f"Extracted Text: {extract_plain_text(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)}")
