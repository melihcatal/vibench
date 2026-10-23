from google.cloud import documentai

def extract_layout_elements(project_id: str, location: str, processor_id: str, file_content: bytes, mime_type: str):
    """
    Extracts layout elements (blocks, lines, tables) from a document using Google Cloud Document AI.
    """
    # Instantiate a Document AI client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor, e.g.:
    # projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    document = {"content": file_content, "mime_type": mime_type}

    # Configure the process request
    request = {"name": resource_name, "document": document}

    # Use the Document AI client to process the document
    result = client.process_document(request=request)

    document_response = result.document

    # For demonstration, we'll just return a simplified representation of text and entities
    # In a real application, you would parse document_response for blocks, lines, tables, etc.
    return {
        "text": document_response.text,
        "entities": [
            {"type": entity.type_, "mention_text": entity.mention_text}
            for entity in document_response.entities
        ],
    }
