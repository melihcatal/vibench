from google.cloud import documentai
from document_client import get_document_ai_client
from document_models import ExtractedInvoice, InvoiceLineItem


def extract_invoice_fields(file_path: str) -> ExtractedInvoice:
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

    line_items = []
    for item_entity in line_item_entities:
        item_details = {
            prop.type_: prop.mention_text for prop in item_entity.properties
        }
        line_items.append(
            InvoiceLineItem(
                description=item_details.get("line_item/description"),
                quantity=float(item_details.get("line_item/quantity", 0)),
                unit_price=float(item_details.get("line_item/unit_price", 0)),
                amount=float(item_details.get("line_item/amount", 0)),
            )
        )

    total_amount_str = raw_fields.get("total_amount", "0").replace("$", "")

    return ExtractedInvoice(
        vendor_name=raw_fields.get("supplier_name"),
        invoice_date=raw_fields.get("invoice_date"),
        total_amount=float(total_amount_str) if total_amount_str else 0.0,
        line_items=line_items,
        raw_fields=raw_fields,
    )
