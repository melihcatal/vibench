from google.cloud import documentai


def extract_layout(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"])})
    layout = []
    for page in response.document.pages:
        for block in page.blocks:
            layout.append({
                "block_type": block.block_type,
                "text": block.text,
                "confidence": block.confidence,
                "bounding_box": block.bounding_box
            })
    return {"layout": layout}