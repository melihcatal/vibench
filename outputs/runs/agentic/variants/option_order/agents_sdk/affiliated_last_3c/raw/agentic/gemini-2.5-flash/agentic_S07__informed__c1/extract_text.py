import os
from google.cloud import documentai_v1 as documentai

def extract_text_from_document(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts plain text from a document using Google Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf",  # Or other appropriate MIME type
        ),
    )

    result = client.process_document(request=request)
    document = result.document
    return document.text

if __name__ == '__main__':
    # Replace with your project details and file path
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"  # e.g., "us"
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID_OCR")  # A "FORM_PARSER" or "OCR_PROCESSOR" type processor
    file_to_process = "path/to/your/document.pdf"

    if project_id and processor_id and os.path.exists(file_to_process):
        extracted_text = extract_text_from_document(project_id, location, processor_id, file_to_process)
        print("Extracted Text:")
        print(extracted_text)
    else:
        print("Please set GOOGLE_CLOUD_PROJECT, DOCUMENT_AI_PROCESSOR_ID_OCR environment variables and ensure document file exists.")
