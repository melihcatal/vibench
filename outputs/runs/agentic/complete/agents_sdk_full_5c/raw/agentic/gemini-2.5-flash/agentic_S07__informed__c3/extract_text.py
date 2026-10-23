import os
from google.cloud import documentai_v1beta3 as documentai

def extract_text(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts plain text from a document using Google Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document.text

if __name__ == '__main__':
    # Placeholder for direct execution, usually integrated via another script
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us" # e.g., "us"
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID_OCR") # A general OCR processor

    # Example: Replace with an actual document path
    # text = extract_text(project_id, location, processor_id, "path/to/your/document.pdf")
    # print("Extracted Text:", text)
