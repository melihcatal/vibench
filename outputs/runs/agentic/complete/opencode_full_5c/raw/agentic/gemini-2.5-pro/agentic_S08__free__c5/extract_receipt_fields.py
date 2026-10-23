from google.cloud import documentai
from document_client import get_document_ai_client
from document_models import ExtractedReceipt, ReceiptItem


def extract_receipt_fields(file_path: str) -> ExtractedReceipt:
    # This assumes the DOCUMENTAI_PROCESSOR_ID is set for a receipt processor
    # e.g. projects/PROJECT_ID/locations/LOCATION/processors/RECEIPT_PROCESSOR_ID
    client, name = get_document_ai_client()

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    raw_fields = {entity.type_: entity.mention_text for entity in document.entities}

    line_item_entities = [
        entity for entity in document.entities if entity.type_ == "line_item"
    ]
    items = []
    for item_entity in line_item_entities:
        item_details = {
            prop.type_: prop.mention_text for prop in item_entity.properties
        }
        items.append(
            ReceiptItem(
                description=item_details.get("line_item/description"),
                quantity=float(item_details.get("line_item/quantity", 0)),
                price=float(item_details.get("line_item/price", 0)),
                total_price=float(item_details.get("line_item/total_price", 0)),
            )
        )

    total_str = raw_fields.get("total_amount", "0").replace("$", "")
    tax_str = raw_fields.get("total_tax_amount", "0").replace("$", "")

    return ExtractedReceipt(
        merchant_name=raw_fields.get("supplier_name"),
        total=float(total_str) if total_str else 0.0,
        tax=float(tax_str) if tax_str else 0.0,
        items=items,
        raw_fields=raw_fields,
    )
