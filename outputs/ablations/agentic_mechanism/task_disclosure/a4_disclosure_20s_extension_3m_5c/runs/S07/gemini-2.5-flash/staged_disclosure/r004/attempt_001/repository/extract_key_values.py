from google.cloud import documentai_v1 as documentai

def extract_key_values_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
) -> dict:
    """
    Extracts key-value pairs from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of the form parser processor.
        file_content: The content of the document file (e.g., PDF, TIFF) as bytes.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        A dictionary containing the extracted key-value pairs.
    """

    # Create a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    document = documentai.RawDocument(content=file_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=document)

    # Use the client to process the document
    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = {}
    for page in document.pages:
        for form_field in page.form_fields:
            field_name = form_field.field_name.text_anchor.content
            field_value = form_field.field_value.text_anchor.content if form_field.field_value else ""
            key_value_pairs[field_name] = field_value
    return key_value_pairs
