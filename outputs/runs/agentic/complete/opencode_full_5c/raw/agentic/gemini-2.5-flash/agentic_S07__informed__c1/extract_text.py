from google.cloud import documentai_v1b3 as documentai
import os


def extract_text(project_id: str, location: str, processor_id: str, file_path: str):
    """Extracts plain text from a document using Google Document AI."""
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

    return document.text


if __name__ == "__main__":
    # Example usage (replace with your actual values)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us"  # e.g., "us"
    PROCESSOR_ID = "YOUR_PROCESSOR_ID"  # Create a "OCR_PROCESSOR" in Document AI
    FILE_PATH = "path/to/your/document.pdf"

    if PROJECT_ID and PROCESSOR_ID and os.path.exists(FILE_PATH):
        extracted_text = extract_text(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
        print("Extracted Text:\n", extracted_text)
    else:
        print(
            "Please set GOOGLE_CLOUD_PROJECT, PROCESSOR_ID, and provide a valid FILE_PATH."
        )
