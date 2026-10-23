from google.cloud import documentai


def validate_document_fields(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"])} )
    required = {"vendor", "date", "total"}
    extracted = {}
    confidences = {}
    for entity in response.document.entities:
        key = entity.type_.replace("supplier_name", "vendor").replace("invoice_date", "date").replace("merchant_name", "vendor").replace("total_amount", "total")
        extracted[key] = entity.mention_text
        confidences[key] = getattr(entity, "confidence", None)
    missing = [field for field in required if not extracted.get(field)]
    low_confidence = [field for field, score in confidences.items() if score is not None and score < 0.8]
    return {"valid": not missing and not low_confidence, "missing": missing, "low_confidence": low_confidence, "fields": extracted}
