from google.cloud import documentai_v1 as documentai
import os

def extract_structured_fields(document_text: str, project_id: str, location: str, processor_id: str):
    """
    Extracts structured fields from OCR-normalized document text using Google Cloud Document AI.

    Args:
        document_text: The OCR-normalized text from the document.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region (e.g., "us").
        processor_id: The ID of the Document AI processor to use (e.g., a Form Parser).

    Returns:
        A Document object containing the extracted entities and form fields.
    """

    # Initialize Document AI client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    name = client.processor_path(project_id, location, processor_id)

    # Convert the text to bytes for Document AI processing
    document_content = document_text.encode("utf-8")

    # Create the document request
    document = documentai.RawDocument(content=document_content, mime_type="text/plain")

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=document)

    # Process the document
    result = client.process_document(request=request)

    # Return the Document object, which contains the extracted fields
    return result.document

