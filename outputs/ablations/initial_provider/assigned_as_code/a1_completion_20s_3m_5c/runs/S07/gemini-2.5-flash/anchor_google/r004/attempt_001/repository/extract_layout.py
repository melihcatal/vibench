from google.cloud import documentai
from google.cloud.documentai_v1 import Document

def extract_layout(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    
    document = documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"]
    )

    request = documentai.ProcessRequest(name=name, raw_document=document)
    response = client.process_document(request=request)

    # Extract layout information (e.g., pages, blocks, paragraphs, lines, tokens)
    # The Document object contains the full hierarchical layout.
    # For simplicity, we'll return a serialized version of the document structure.
    # In a real scenario, you'd process response.document to extract specific layout elements.
    return Document.to_json(response.document)
