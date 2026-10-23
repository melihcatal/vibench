
from google.cloud import documentai_v1 as documentai

def extract_fields_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    document_content: bytes,
    mime_type: str = "application/pdf",
):
    """
    Extracts structured fields from OCR-normalized document text using Google Cloud Document AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region (e.g., "us").
        processor_id (str): The ID of the Document AI processor to use.
        document_content (bytes): The content of the document (e.g., PDF bytes).
        mime_type (str): The MIME type of the document (e.g., "application/pdf").

    Returns:
        documentai.Document: The processed document with extracted entities.
    """

    # Create a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    document = documentai.RawDocument(content=document_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=document)

    # Use the Document AI client to process the document
    result = client.process_document(request=request)

    return result.document

