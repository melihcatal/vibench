from google.cloud import documentai_v1 as documentai

def extract_key_values_from_document(project_id: str, location: str, processor_id: str, image_content: bytes) -> list[documentai.Document.Page.FormField]:
    """Extracts key-value pairs from a form-like document using Google Cloud Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    
    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=image_content, mime_type="image/jpeg")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    response = client.process_document(request=request)
    
    key_value_pairs = []
    for page in response.document.pages:
        key_value_pairs.extend(page.form_fields)
    return key_value_pairs
