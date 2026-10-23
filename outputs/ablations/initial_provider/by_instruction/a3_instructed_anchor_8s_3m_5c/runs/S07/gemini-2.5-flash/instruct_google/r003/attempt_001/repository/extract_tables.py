from google.cloud import documentai_v1 as documentai

def extract_tables_from_document(project_id: str, location: str, processor_id: str, image_content: bytes) -> list[documentai.Document.Page.Table]:
    """Extracts table cells and row structure from a document using Google Cloud Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    
    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=image_content, mime_type="image/jpeg")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    response = client.process_document(request=request)
    
    tables = []
    for page in response.document.pages:
        tables.extend(page.tables)
    return tables
