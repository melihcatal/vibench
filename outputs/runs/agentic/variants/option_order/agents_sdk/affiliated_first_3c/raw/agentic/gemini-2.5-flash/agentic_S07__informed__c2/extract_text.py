from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os

def extract_text(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> str:
    """Extracts plain text from a document using Google Document AI."""

    # You would typically get these from environment variables or a config file
    # For demonstration, hardcoding Google Document AI endpoint
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    return document.text

if __name__ == '__main__':
    # Placeholder for actual usage, replace with your project details and a dummy file
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # Example processor ID for general OCR: "ocrembedded-v2.0-2020-09-23" or "pretrained-ocr-v1.0"
    # For a general processor, you might need to create one in the console.
    # For a general text extraction, "form-parser" or "pretrained-ocr-v1.0" are good starting points.
    # A generic "OCR Processor" can be created in Document AI console.
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = "us" # e.g., "us"
    processor_id = os.getenv("DOCUMENTAI_OCR_PROCESSOR_ID", "your-ocr-processor-id") # e.g., "YOUR_OCR_PROCESSOR_ID"
    
    # Create a dummy image file for testing
    dummy_file_path = "dummy.png"
    with open(dummy_file_path, "wb") as f:
        f.write(b"dummy image content") # Replace with actual image content for real testing

    try:
        # result_text = extract_text(project_id, location, processor_id, dummy_file_path, "image/png")
        # print(f"Extracted Text: {result_text}")
        print("Run with actual Document AI credentials and a valid processor ID and image file.")
    except Exception as e:
        print(f"Error extracting text: {e}")
    finally:
        os.remove(dummy_file_path)
