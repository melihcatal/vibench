import os
from typing import Optional

from google.cloud import documentai

from document_client import get_documentai_client
from document_models import Invoice, LineItem


def extract_invoice_fields_from_document(
    file_path: str, mime_type: str
) -> Optional[Invoice]:
    client, project_id, location = get_documentai_client()

    processor_id = os.getenv("INVOICE_PROCESSOR_ID")
    if not processor_id:
        raise ValueError("INVOICE_PROCESSOR_ID environment variable not set.")

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    if not document.entities:
        return None

    entity_map = {entity.type_: entity.mention_text for entity in document.entities}

    line_item_entities = [
        entity for entity in document.entities if entity.type_ == "line_item"
    ]
    line_items = []
    for item_entity in line_item_entities:
        item_details = {
            prop.type_: prop.mention_text for prop in item_entity.properties
        }
        line_items.append(
            LineItem(
                description=item_details.get("line_item/description", ""),
                quantity=float(item_details.get("line_item/quantity", 0)),
                unit_price=float(item_details.get("line_item/unit_price", 0)),
                amount=float(item_details.get("line_item/amount", 0)),
            )
        )

    return Invoice(
        vendor_name=entity_map.get("vendor_name"),
        invoice_id=entity_map.get("invoice_id"),
        invoice_date=entity_map.get("invoice_date"),
        due_date=entity_map.get("due_date"),
        subtotal=float(entity_map.get("net_amount", 0)),
        tax=float(entity_map.get("tax_amount", 0)),
        total=float(entity_map.get("total_amount", 0)),
        currency=entity_map.get("currency"),
        line_items=line_items,
    )
