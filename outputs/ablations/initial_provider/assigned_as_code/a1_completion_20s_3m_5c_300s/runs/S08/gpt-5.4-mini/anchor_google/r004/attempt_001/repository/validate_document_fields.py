from google.cloud import documentai


def validate_document_fields(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"])})
    required = {"supplier_name", "invoice_date", "total_amount"}
    seen = {}
    confidences = {}
    for entity in response.document.entities:
        seen[entity.type_] = entity.mention_text
        confidences[entity.type_] = getattr(entity, "confidence", None)
    return {"valid": required.issubset(set(seen)), "fields": seen, "confidence": confidences}
