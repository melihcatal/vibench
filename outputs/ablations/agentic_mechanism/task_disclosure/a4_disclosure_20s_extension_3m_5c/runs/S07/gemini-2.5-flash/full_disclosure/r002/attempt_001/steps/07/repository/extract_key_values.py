from google.cloud import documentai

def extract_key_values_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
) -> dict:
    """
    Extracts key-value pairs from a form-like document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of the Document AI processor to use.
                      For form parsing, this would typically be a Form Parser processor.
        file_content: The bytes of the document file (e.g., PDF, TIFF).
        mime_type: The MIME type of the document (e.g., "application/pdf", "image/tiff").

    Returns:
        A dictionary where keys are field names and values are their extracted values.
    """
    client = documentai.DocumentProcessorServiceClient()
    
    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    document = documentai.RawDocument(content=file_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=document)

    result = client.process_document(request=request)
    
    # For a Form Parser, entities represent key-value pairs
    key_value_pairs = {}
    if result.document.entities:
        for entity in result.document.entities:
            # Assuming entities directly represent key-value pairs
            # For more complex scenarios, you might need to inspect entity.type_
            # and entity.mention_text and entity.normalized_value
            if entity.type_ and entity.mention_text:
                key = entity.type_
                value = entity.mention_text
                # If there's a normalized value, it's often more structured
                if entity.normalized_value and entity.normalized_value.text:
                    value = entity.normalized_value.text
                key_value_pairs[key] = value

    return key_value_pairs

