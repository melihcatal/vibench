from google.cloud import documentai

from document_models import normalize_expense_record


def normalize_expense(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"])} )
    fields = {entity.type_: entity.mention_text for entity in response.document.entities if entity.type_ != "line_item"}
    items = []
    for entity in response.document.entities:
        if entity.type_ == "line_item":
            values = {p.type_.split("/")[-1]: p.mention_text for p in entity.properties}
            items.append({"description": values.get("description"), "quantity": values.get("quantity"), "amount": values.get("amount")})
    return normalize_expense_record({"vendor": fields.get("supplier_name") or fields.get("merchant_name"), "date": fields.get("invoice_date") or fields.get("receipt_date"), "total": fields.get("total_amount"), "tax": fields.get("total_tax"), "items": items})
