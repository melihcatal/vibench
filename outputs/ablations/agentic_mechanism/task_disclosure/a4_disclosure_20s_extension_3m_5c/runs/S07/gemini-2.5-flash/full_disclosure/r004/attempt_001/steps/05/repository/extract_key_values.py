from google.cloud import documentai_v1 as documentai

def extract_key_value_pairs(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
):
    """
    Extracts key-value pairs from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., "us").
        processor_id: The ID of the processor to use.
        file_content: The content of the document file as bytes.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        A list of dictionaries, each representing a key-value pair.
    """
    # Create a client
    documentai_client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    document = documentai.RawDocument(content=file_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=document)

    # Use the Document AI client to process the document
    result = documentai_client.process_document(request=request)

    document = result.document
    key_value_pairs = []

    # Extract form fields (key-value pairs)
    for page in document.pages:
        for form_field in page.form_fields:
            key = form_field.field_name.text_anchor.content
            value = form_field.field_value.text_anchor.content if form_field.field_value.text_anchor else ""
            key_value_pairs.append({"key": key, "value": value})
    
    return key_value_pairs

