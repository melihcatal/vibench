from typing import List, Optional
import os
from document_client import get_documentai_client
from document_models import Invoice, LineItem


def extract_invoice_fields(file_path: str) -> Optional[Invoice]:
    """
    Extracts fields from an invoice document using Google Document AI.
    """
    client = get_documentai_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.environ.get("DOCAI_INVOICE_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError("Missing Google Cloud or Document AI configuration.")

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = {"content": image_content, "mime_type": "application/pdf"}

    request = {"name": name, "raw_document": raw_document}
    result = client.process_document(request=request)
    document = result.document

    invoice = Invoice()
    for entity in document.entities:
        if entity.type_ == "supplier_name":
            invoice.vendor_name = entity.mention_text
        elif entity.type_ == "invoice_date":
            invoice.invoice_date = entity.mention_text
        elif entity.type_ == "total_amount":
            invoice.total_amount = float(entity.mention_text.replace("$", ""))

    for entity in document.entities:
        if entity.type_ == "line_item":
            line_item = LineItem(description="", amount=0.0)
            for prop in entity.properties:
                if prop.type_ == "line_item/description":
                    line_item.description = prop.mention_text
                elif prop.type_ == "line_item/amount":
                    line_item.amount = float(prop.mention_text.replace("$", ""))
            if line_item.description:
                invoice.line_items.append(line_item)

    return invoice
