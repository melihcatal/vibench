
import os
from google.cloud import documentai_v1 as documentai

def get_document_processor_client():
    """
    Returns a Document AI client for OCR and layout extraction.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return documentai.DocumentProcessorServiceClient()

def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
):
    """
    Processes a document using the Document AI processor.

    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., "us").
        processor_id: The ID of the processor to use.
        file_path: The path to the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        A Document object containing the processed document.
    """
    client = get_document_processor_client()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document

if __name__ == "__main__":
    # Example Usage (replace with your actual values)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"

    # project_id = "your-project-id"
    # location = "us"  # e.g., "us" or "eu"
    # processor_id = "your-processor-id"  # e.g., "YOUR_PROCESSOR_ID"
    # document_path = "path/to/your/document.pdf"
    # document_mime_type = "application/pdf"

    # try:
    #     document = process_document(
    #         project_id, location, processor_id, document_path, document_mime_type
    #     )
    #     print("Document processing successful!")
    #     print(f"Text: {document.text[:500]}...")  # Print first 500 characters
    #     # You can further process document.pages, document.entities, etc.
    # except Exception as e:
    #     print(f"Error processing document: {e}")
