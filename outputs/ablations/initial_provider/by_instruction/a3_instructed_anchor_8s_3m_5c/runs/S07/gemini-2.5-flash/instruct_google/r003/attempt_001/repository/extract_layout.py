from google.cloud import documentai_v1 as documentai

def extract_layout_from_document(project_id: str, location: str, processor_id: str, image_content: bytes) -> documentai.Document:
    """Extracts layout elements from a document using Google Cloud Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    
    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=image_content, mime_type="image/jpeg") # Assuming JPEG for now
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    response = client.process_document(request=request)
    return response.document
