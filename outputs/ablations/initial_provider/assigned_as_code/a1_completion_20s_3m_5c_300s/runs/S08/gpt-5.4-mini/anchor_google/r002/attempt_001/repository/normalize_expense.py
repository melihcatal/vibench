from google.cloud import documentai

from document_models import normalize_fields


def normalize_expense(payload, config=None):
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
    data = {entity.type_: entity.mention_text for entity in response.document.entities}
    return {"expense": normalize_fields({"vendor": data.get("supplier_name") or data.get("merchant_name"), "date": data.get("invoice_date") or data.get("receipt_date"), "total": data.get("total_amount"), "currency": data.get("currency")})}
