from google.cloud import documentai_v1 as documentai

def extract_structured_fields(project_id: str, location: str, processor_id: str, document_text: str) -> documentai.Document:
    """Extracts structured fields from OCR-normalized document text using Google Cloud Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    
    name = client.processor_path(project_id, location, processor_id)

    # For text input, we create a Document object directly
    document = documentai.Document(text=document_text, mime_type="text/plain")
    request = documentai.ProcessRequest(name=name, document=document)

    response = client.process_document(request=request)
    return response.document
