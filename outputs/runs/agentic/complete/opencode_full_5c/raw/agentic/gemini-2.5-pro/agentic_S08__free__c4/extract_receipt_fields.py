import os
from typing import Optional

from google.cloud import documentai

from document_client import get_documentai_client
from document_models import Document, Receipt, LineItem


def extract_receipt_fields(
    document: Document,
    project_id: Optional[str] = None,
    processor_id: Optional[str] = None,
    location: str = "us",
) -> Receipt:
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    processor_id = processor_id or os.getenv("RECEIPT_PROCESSOR_ID")

    if not project_id or not processor_id:
        raise ValueError("Project ID and Processor ID must be provided.")

    client = get_documentai_client()

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document.content, mime_type=document.mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    doc = result.document

    receipt = Receipt()
    for entity in doc.entities:
        if entity.type_ == "supplier_name":
            receipt.merchant_name = entity.mention_text
        elif entity.type_ == "transaction_date":
            receipt.transaction_date = entity.mention_text
        elif entity.type_ == "total_tax_amount":
            try:
                receipt.tax_amount = float(entity.mention_text.replace("$", ""))
            except (ValueError, TypeError):
                receipt.tax_amount = None
        elif entity.type_ == "total_amount":
            try:
                receipt.total_amount = float(entity.mention_text.replace("$", ""))
            except (ValueError, TypeError):
                receipt.total_amount = None
        elif entity.type_ == "line_item":
            line_item = LineItem()
            for prop in entity.properties:
                if prop.type_ == "line_item_description":
                    line_item.description = prop.mention_text
                elif prop.type_ == "line_item_quantity":
                    try:
                        line_item.quantity = float(prop.mention_text)
                    except (ValueError, TypeError):
                        pass
                elif prop.type_ == "line_item_unit_price":
                    try:
                        line_item.unit_price = float(prop.mention_text.replace("$", ""))
                    except (ValueError, TypeError):
                        pass
                elif prop.type_ == "line_item_amount":
                    try:
                        line_item.total_amount = float(
                            prop.mention_text.replace("$", "")
                        )
                    except (ValueError, TypeError):
                        pass
            receipt.line_items.append(line_item)

    return receipt
