from typing import List
from document_client import DocumentAIClient
from document_models import Invoice, InvoiceLineItem


def extract_invoice_fields(
    file_content: bytes, mime_type: str = "application/pdf"
) -> Invoice:
    client = DocumentAIClient()
    document = client.process_document("INVOICE_PROCESSOR", file_content, mime_type)

    vendor_name = ""
    invoice_date = ""
    total_amount = 0.0
    line_items_list = []
    doc_confidence = 0.0

    if document.entities:
        doc_confidence = document.confidence
        for entity in document.entities:
            if entity.type_ == "supplier_name":
                vendor_name = entity.mention_text
            elif entity.type_ == "invoice_date":
                invoice_date = (
                    entity.normalized_value.text
                    if entity.normalized_value
                    else entity.mention_text
                )
            elif entity.type_ == "total_amount":
                total_amount = (
                    float(entity.normalized_value.text.replace("$", ""))
                    if entity.normalized_value
                    else 0.0
                )
            elif entity.type_ == "line_item":
                line_item = {}
                for prop in entity.properties:
                    if prop.type_ == "line_item/description":
                        line_item["description"] = prop.mention_text
                    elif prop.type_ == "line_item/quantity":
                        line_item["quantity"] = (
                            float(prop.mention_text) if prop.mention_text else 0.0
                        )
                    elif prop.type_ == "line_item/unit_price":
                        line_item["unit_price"] = (
                            float(prop.mention_text) if prop.mention_text else 0.0
                        )
                    elif prop.type_ == "line_item/amount":
                        line_item["amount"] = (
                            float(prop.mention_text.replace("$", ""))
                            if prop.mention_text
                            else 0.0
                        )
                if line_item:
                    line_items_list.append(InvoiceLineItem(**line_item))

    return Invoice(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        total_amount=total_amount,
        line_items=line_items_list,
        confidence=doc_confidence,
    )
