
from google.cloud import documentai_v1beta3 as documentai

def extract_fields_from_document(project_id: str, location: str, processor_id: str, file_content: bytes, mime_type: str):
    """
    Extracts structured fields from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., "us").
        processor_id: The ID of the processor to use (e.g., a Form Parser or Custom Extractor).
        file_content: The bytes content of the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf", "image/tiff").

    Returns:
        A Document object containing the extracted fields.
    """
    client = documentai.DocumentProcessorServiceClient()
    
    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processors/processor-id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    document = {"content": file_content, "mime_type": mime_type}

    # Configure the process request
    request = {"name": resource_name, "document": document}

    # Use the Document AI client to process the document
    result = client.process_document(request=request)

    return result.document

