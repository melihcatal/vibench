from google.cloud import documentai


def validate_document_fields(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"}
    )
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(
        request={
            "name": name,
            "raw_document": documentai.RawDocument(
                content=payload["document_bytes"], mime_type=payload["mime_type"]
            ),
        }
    )
    entities = {entity.type_: entity.confidence for entity in response.document.entities}
    required = ["supplier_name", "invoice_date", "total_amount"]
    return {"valid": all(key in entities and entities[key] is not None for key in required), "confidence_scores": entities}
