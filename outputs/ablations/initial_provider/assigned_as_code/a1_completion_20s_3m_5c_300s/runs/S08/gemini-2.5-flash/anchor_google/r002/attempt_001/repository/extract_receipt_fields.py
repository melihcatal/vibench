from google.cloud import documentai
from document_client import get_documentai_client
from document_models import Receipt, ReceiptItem

def extract_receipt_fields(payload: dict, config: dict = None) -> dict:
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    location = config.get("location", "us")
    processor_id = config.get("processor_id")

    if not project_id or not processor_id:
        raise ValueError("Google Cloud project_id and processor_id must be provided.")

    client = get_documentai_client(location)
    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"]
    )
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    response = client.process_document(request=request)

    receipt_fields = {
        "merchant": None,
        "total": None,
        "tax": None,
        "items": [],
        "date": None
    }
    
    for entity in response.document.entities:
        if entity.type_ == "line_item":
            item_values = {
                prop.type_.split("/")[-1]: prop.mention_text
                for prop in entity.properties
            }
            receipt_fields["items"].append(
                ReceiptItem(
                    description=item_values.get("description"),
                    quantity=float(item_values["quantity"]) if item_values.get("quantity") else None,
                    price=float(item_values["unit_price"]) if item_values.get("unit_price") else None,
                    amount=float(item_values["amount"]) if item_values.get("amount") else None,
                ).dict(exclude_none=True)
            )
        elif entity.type_ == "total_amount":
            receipt_fields["total"] = float(entity.mention_text) if entity.mention_text else None
        elif entity.type_ == "tax_amount":
            receipt_fields["tax"] = float(entity.mention_text) if entity.mention_text else None
        elif entity.type_ == "merchant_name":
            receipt_fields["merchant"] = entity.mention_text
        elif entity.type_ == "transaction_date":
            receipt_fields["date"] = entity.mention_text

    return {"receipts": [Receipt(**receipt_fields).dict(exclude_none=True)]}
