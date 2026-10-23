from google.cloud import documentai
from google.cloud.documentai_v1 import Document

def extract_tables(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    
    document = documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"]
    )

    request = documentai.ProcessRequest(name=name, raw_document=document)
    response = client.process_document(request=request)

    # Extract table information
    # The Document object contains tables within response.document.pages[i].tables
    # For simplicity, we'll return a serialized version of the document structure
    # including tables. In a real scenario, you'd iterate through tables and cells.
    return Document.to_json(response.document)
