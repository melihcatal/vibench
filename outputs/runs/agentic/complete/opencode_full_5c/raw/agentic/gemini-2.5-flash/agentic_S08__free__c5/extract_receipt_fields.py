import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_documentai_processor_path
from document_models import DocumentField, LineItem, ReceiptExtractionResult


def extract_receipt_fields(
    project_id: str, location: str, processor_id: str, file_path: str
) -> ReceiptExtractionResult:
    client = get_documentai_client()
    processor_path = get_documentai_processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image_file:
        image_content = image_file.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )  # Assuming PDF/image receipts

    request = documentai.ProcessRequest(name=processor_path, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    fields: Dict[str, DocumentField] = {}
    line_items: List[LineItem] = []

    def _get_field_value(field) -> DocumentField:
        return DocumentField(
            value=field.text_anchor.content if field.text_anchor.content else None,
            confidence=field.confidence,
        )

    def _get_entity_value(entity):
        return (
            entity.text_anchor.content
            if entity.text_anchor.content
            else entity.mention_text
        )

    for entity in document.entities:
        if entity.type == "merchant_name":
            fields["merchant_name"] = _get_field_value(entity)
        elif entity.type == "transaction_date":
            fields["transaction_date"] = _get_field_value(entity)
        elif entity.type == "total_amount":
            fields["total_amount"] = _get_field_value(entity)
            if entity.normalized_value and entity.normalized_value.money_value:
                fields["currency"] = DocumentField(
                    value=entity.normalized_value.money_value.currency_code,
                    confidence=entity.confidence,
                )
            else:
                fields["currency"] = DocumentField(value=None, confidence=0.0)
        elif entity.type == "tax_amount":
            fields["tax_amount"] = _get_field_value(entity)
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
        elif entity.type == "receipt_id":
            fields["receipt_id"] = _get_field_value(entity)

    return ReceiptExtractionResult(
        merchant_name=fields.get("merchant_name", DocumentField()),
        transaction_date=fields.get("transaction_date", DocumentField()),
        total_amount=fields.get("total_amount", DocumentField()),
        currency=fields.get("currency", DocumentField()),
        tax_amount=fields.get("tax_amount"),
        line_items=line_items,
        receipt_id=fields.get("receipt_id"),
    )
