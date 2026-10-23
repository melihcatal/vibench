from typing import List
from document_client import DocumentAIClient
from document_models import Receipt, ReceiptItem


def extract_receipt_fields(
    file_content: bytes, mime_type: str = "application/pdf"
) -> Receipt:
    client = DocumentAIClient()
    # Using a standard Google Cloud Document AI processor name
    processor_name = "RECEIPT_PROCESSOR"
    document = client.process_document(processor_name, file_content, mime_type)

    merchant_name = ""
    transaction_date = ""
    tax_amount = 0.0
    total_amount = 0.0
    items_list = []
    doc_confidence = 0.0

    if document.entities:
        doc_confidence = document.confidence
        for entity in document.entities:
            if entity.type_ == "supplier_name":
                merchant_name = entity.mention_text
            elif entity.type_ == "transaction_date":
                transaction_date = (
                    entity.normalized_value.text
                    if entity.normalized_value
                    else entity.mention_text
                )
            elif entity.type_ == "total_tax_amount":
                tax_amount = (
                    float(entity.normalized_value.text.replace("$", ""))
                    if entity.normalized_value and entity.normalized_value.text
                    else 0.0
                )
            elif entity.type_ == "total_amount":
                total_amount = (
                    float(entity.normalized_value.text.replace("$", ""))
                    if entity.normalized_value and entity.normalized_value.text
                    else 0.0
                )
            elif entity.type_ == "line_item":
                item_details = {}
                for prop in entity.properties:
                    if prop.type_ == "line_item/description":
                        item_details["description"] = prop.mention_text
                    elif prop.type_ == "line_item/quantity":
                        item_details["quantity"] = (
                            float(prop.mention_text) if prop.mention_text else 1.0
                        )
                    elif prop.type_ == "line_item/unit_price":
                        item_details["price"] = (
                            float(prop.mention_text) if prop.mention_text else 0.0
                        )
                    elif prop.type_ == "line_item/amount":
                        item_details["total"] = (
                            float(prop.mention_text) if prop.mention_text else 0.0
                        )
                if "description" in item_details:
                    items_list.append(ReceiptItem(**item_details))

    return Receipt(
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        tax_amount=tax_amount,
        total_amount=total_amount,
        items=items_list,
        confidence=doc_confidence,
    )
