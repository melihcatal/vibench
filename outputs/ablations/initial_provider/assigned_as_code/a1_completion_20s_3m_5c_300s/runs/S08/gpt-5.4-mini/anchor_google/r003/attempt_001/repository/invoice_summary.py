from google.cloud import documentai


def invoice_summary(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"}
    )
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"] )})
    total = None
    vendor = None
    for entity in response.document.entities:
        if entity.type_ == "total_amount":
            total = entity.mention_text
        if entity.type_ == "supplier_name":
            vendor = entity.mention_text
    return {"summary": f"Invoice from {vendor} with total {total}"}
