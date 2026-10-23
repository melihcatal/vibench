import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_documentai_processor_path
from document_models import DocumentField, LineItem, InvoiceExtractionResult


def extract_invoice_fields(
    project_id: str, location: str, processor_id: str, file_path: str
) -> InvoiceExtractionResult:
    client = get_documentai_client()
    processor_path = get_documentai_processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image_file:
        image_content = image_file.read()

    # Create a Document object
    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )  # Assuming PDF invoices

    # Configure the process request
    request = documentai.ProcessRequest(name=processor_path, raw_document=raw_document)

    # Use the Document AI client to process the document
    result = client.process_document(request=request)
    document = result.document

    # Extract fields
    fields: Dict[str, DocumentField] = {}
    line_items: List[LineItem] = []

    def _get_field_value(field) -> DocumentField:
        return DocumentField(
            value=field.text_anchor.content if field.text_anchor.content else None,
            confidence=field.confidence,
        )

    def _get_entity_value(entity):
        # Helper to extract value from Document AI entity
        return (
            entity.text_anchor.content
            if entity.text_anchor.content
            else entity.mention_text
        )

    for entity in document.entities:
        if entity.type == "vendor_name":
            fields["vendor_name"] = _get_field_value(entity)
        elif entity.type == "invoice_date":
            fields["invoice_date"] = _get_field_value(entity)
        elif entity.type == "total_amount":
            fields["total_amount"] = _get_field_value(entity)
            if entity.normalized_value and entity.normalized_value.money_value:
                fields["currency"] = DocumentField(
                    value=entity.normalized_value.money_value.currency_code,
                    confidence=entity.confidence,
                )
            else:
                fields["currency"] = DocumentField(value=None, confidence=0.0)
        elif entity.type == "line_item":
            item_data = {}
            item_data["confidence"] = entity.confidence
            for prop in entity.properties:
                if prop.type == "description":
                    item_data["description"] = _get_entity_value(prop)
                elif prop.type == "quantity":
                    item_data["quantity"] = (
                        float(_get_entity_value(prop))
                        if _get_entity_value(prop)
                        else None
                    )
                elif prop.type == "unit_price":
                    item_data["unit_price"] = (
                        float(_get_entity_value(prop))
                        if _get_entity_value(prop)
                        else None
                    )
                elif prop.type == "total_price":
                    item_data["total_price"] = (
                        float(_get_entity_value(prop))
                        if _get_entity_value(prop)
                        else None
                    )
                elif prop.type == "currency":
                    item_data["currency"] = _get_entity_value(prop)
            line_items.append(LineItem(**item_data))
        elif entity.type == "purchase_order":
            fields["purchase_order"] = _get_field_value(entity)
        elif entity.type == "vendor_address":
            fields["vendor_address"] = _get_field_value(entity)
        elif entity.type == "due_date":
            fields["due_date"] = _get_field_value(entity)
        elif entity.type == "invoice_id":
            fields["invoice_id"] = _get_field_value(entity)
        elif entity.type == "notes":
            fields["notes"] = _get_field_value(entity)

    return InvoiceExtractionResult(
        vendor_name=fields.get("vendor_name", DocumentField()),
        invoice_date=fields.get("invoice_date", DocumentField()),
        total_amount=fields.get("total_amount", DocumentField()),
        currency=fields.get("currency", DocumentField()),
        line_items=line_items,
        purchase_order=fields.get("purchase_order"),
        vendor_address=fields.get("vendor_address"),
        due_date=fields.get("due_date"),
        invoice_id=fields.get("invoice_id"),
        notes=fields.get("notes"),
    )
