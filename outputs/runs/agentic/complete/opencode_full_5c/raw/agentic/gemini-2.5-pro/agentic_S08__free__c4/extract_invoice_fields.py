import os
from typing import Optional

from google.cloud import documentai

from document_client import get_documentai_client
from document_models import Document, Invoice, LineItem


def extract_invoice_fields(
    document: Document,
    project_id: Optional[str] = None,
    processor_id: Optional[str] = None,
    location: str = "us",
) -> Invoice:
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    processor_id = processor_id or os.getenv("INVOICE_PROCESSOR_ID")

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

    invoice = Invoice()
    for entity in doc.entities:
        if entity.type_ == "supplier_name":
            invoice.vendor_name = entity.mention_text
        elif entity.type_ == "invoice_date":
            invoice.invoice_date = entity.mention_text
        elif entity.type_ == "total_amount":
            try:
                invoice.total_amount = float(entity.mention_text.replace("$", ""))
            except (ValueError, TypeError):
                invoice.total_amount = None
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
            invoice.line_items.append(line_item)

    return invoice
