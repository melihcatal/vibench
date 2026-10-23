from google.cloud import documentai_v1 as documentai

def extract_tables_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    file_mime_type: str,
) -> documentai.Document:
    """
    Extracts table cells and row structure from a document using Google Cloud Document AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region (e.g., "us").
        processor_id (str): The ID of the Document AI processor configured for table extraction.
        file_path (str): The path to the document file.
        file_mime_type (str): The MIME type of the document (e.g., "application/pdf").

    Returns:
        documentai.Document: The processed document with extracted table data.
    """
    # Instantiates a client
    documentai_client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = documentai_client.processor_path(
        project_id, location, processor_id
    )

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(
            content=image_content, mime_type=file_mime_type
        ),
    )

    result = documentai_client.process_document(request=request)
    return result.document
