import os
from document_client import get_documentai_client
from document_models import Invoice, LineItem
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(file_path: str) -> Invoice:
    client, processor_name = get_documentai_client()

    with open(file_path, "rb") as image_file:
        image_content = image_file.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF, adjust if other types are expected

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    result = client.process_document(request=request)

    document = result.document
    invoice = Invoice()

    # Extracting document-level fields
    for entity in document.entities:
        if entity.type == "vendor_name":
            invoice.vendor_name = entity.mention_text
        elif entity.type == "invoice_date":
            invoice.invoice_date = entity.mention_text
        elif entity.type == "total_amount":
            try:
                invoice.total_amount = float(entity.mention_text)
            except (ValueError, TypeError):
                pass # Handle cases where conversion fails
        elif entity.type == "line_item":
            line_item = LineItem(description=entity.mention_text)
            for prop in entity.properties:
                if prop.type == "description":
                    line_item.description = prop.mention_text
                elif prop.type == "quantity":
                    try:
                        line_item.quantity = float(prop.mention_text)
                    except (ValueError, TypeError):
                        pass
                elif prop.type == "unit_price":
                    try:
                        line_item.unit_price = float(prop.mention_text)
                    except (ValueError, TypeError):
                        pass
                elif prop.type == "total_price":
                    try:
                        line_item.total_price = float(prop.mention_text)
                    except (ValueError, TypeError):
                        pass
            invoice.line_items.append(line_item)

    return invoice
