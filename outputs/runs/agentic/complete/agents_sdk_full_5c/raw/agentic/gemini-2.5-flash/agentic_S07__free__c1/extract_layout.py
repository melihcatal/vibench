import os
from google.cloud import documentai_v1 as documentai

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOCATION = "us"
PROCESSOR_ID_LAYOUT = os.environ.get("GCP_DOCUMENTAI_LAYOUT_PROCESSOR_ID") # e.g., "pretrained-foundation-model"

def extract_layout(image_content: bytes) -> documentai.Document:
    """Extracts layout elements from a document using Google Cloud Document AI's general processor."""
    if not all([PROJECT_ID, PROCESSOR_ID_LAYOUT]):
        raise ValueError("Environment variables GCP_PROJECT_ID, GCP_DOCUMENTAI_LAYOUT_PROCESSOR_ID must be set.")

    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    resource_name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID_LAYOUT)

    # Read the file into memory
    raw_document = documentai.RawDocument(content=image_content, mime_type="image/jpeg")

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document

if __name__ == '__main__':
    # This is a placeholder for demonstration.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS and required env vars are set.
    os.environ["GCP_PROJECT_ID"] = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id") # Replace with your project ID
    os.environ["GCP_DOCUMENTAI_LAYOUT_PROCESSOR_ID"] = os.environ.get("GCP_DOCUMENTAI_LAYOUT_PROCESSOR_ID", "builtin/ocr") # Use 'builtin/ocr' for general OCR/layout

    try:
        with open("example.jpeg", "rb") as image_file:
            content = image_file.read()
        document = extract_layout(content)
        print("Document Pages:", len(document.pages))
        if document.pages:
            print("First page text:\n", document.pages[0].layout.text_anchor.text_segments[0].text if document.pages[0].layout.text_anchor.text_segments else "")
    except FileNotFoundError:
        print("Please create an 'example.jpeg' file or replace the path with a valid image.")
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")
