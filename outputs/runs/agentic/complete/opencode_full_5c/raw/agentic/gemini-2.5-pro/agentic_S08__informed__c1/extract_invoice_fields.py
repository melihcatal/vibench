import os
from typing import Optional
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import Invoice, LineItem


def extract_invoice_fields(
    file_path: str, processor_id: Optional[str] = None
) -> Invoice:
    """
    Extracts fields from an invoice document using Google Document AI.
    """
    client, project_id, location = get_documentai_client()

    if not processor_id:
        processor_id = os.getenv("GOOGLE_INVOICE_PROCESSOR_ID")
        if not processor_id:
            raise ValueError("GOOGLE_INVOICE_PROCESSOR_ID must be set.")

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    invoice = Invoice()
    invoice.raw_fields = documentai.Document.to_dict(document)

    for entity in document.entities:
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
                if prop.type_ == "line_item/description":
                    line_item.description = prop.mention_text
                elif prop.type_ == "line_item/amount":
                    try:
                        line_item.amount = float(prop.mention_text.replace("$", ""))
                    except (ValueError, TypeError):
                        line_item.amount = None
            if any(vars(line_item).values()):
                invoice.line_items.append(line_item)

    return invoice
