from google.cloud import documentai

def extract_fields_from_document_text(
    project_id: str,
    location: str,
    processor_id: str,
    document_text: str,
):
    """
    Extracts structured fields from OCR-normalized document text using Google Cloud Document AI.
    """

    # You would typically create a raw document from the text.
    # For field extraction, you might need a specialized processor, e.g., Form Parser.
    # The Document AI client is used to send the document for processing.

    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Create the document payload.
    document = documentai.Document(content=document_text, mime_type="text/plain")

    # Configure the process request.
    request = documentai.ProcessRequest(name=resource_name, document=document)

    # Process the document.
    result = client.process_document(request=request)

    # For demonstration, we'll just print some basic info if available.
    # In a real application, you would parse result.document.entities for structured fields.
    print(f"Document processing complete. Document ID: {result.document.uri}")
    if result.document.entities:
        print("Extracted Entities:")
        for entity in result.document.entities:
            print(f"  Type: {entity.type_}, Mention Text: {entity.mention_text}")
    else:
        print("No entities extracted.")

    return result.document
