from google.cloud import documentai


def validate_document_fields(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"}
    )
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"] )})
    required = {"supplier_name", "invoice_date", "total_amount"}
    found = {entity.type_ for entity in response.document.entities}
    confidences = {entity.type_: getattr(entity, "confidence", None) for entity in response.document.entities}
    return {"valid": required.issubset(found), "missing": sorted(required - found), "confidence": confidences}
