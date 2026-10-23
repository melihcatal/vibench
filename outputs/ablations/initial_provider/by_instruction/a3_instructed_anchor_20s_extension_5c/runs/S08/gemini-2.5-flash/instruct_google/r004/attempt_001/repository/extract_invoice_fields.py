import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import Invoice, LineItem

def extract_invoice_fields(document_content: bytes, mime_type: str) -> Invoice:
    client = get_documentai_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    processor_id = os.getenv("GOOGLE_CLOUD_INVOICE_PROCESSOR_ID") # Specific processor for invoices

    if not processor_id:
        raise ValueError("GOOGLE_CLOUD_INVOICE_PROCESSOR_ID environment variable must be set.")

    # The full resource name of the processor
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    raw_document = documentai.RawDocument(content=document_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    invoice = Invoice()

    for entity in document.entities:
        if entity.type == "vendor_name":
            invoice.vendor_name = entity.mention_text
        elif entity.type == "invoice_date":
            invoice.invoice_date = entity.mention_text
        elif entity.type == "total_amount":
            # Assuming the total_amount is a float and currency is often associated
            invoice.total_amount = float(entity.mention_text) if entity.mention_text else None
            if entity.normalized_value and entity.normalized_value.currency_symbol:
                invoice.currency = entity.normalized_value.currency_symbol
        elif entity.type == "line_item":
            line_item = LineItem()
            for prop in entity.properties:
                if prop.type == "description":
                    line_item.description = prop.mention_text
                elif prop.type == "quantity":
                    line_item.quantity = float(prop.mention_text) if prop.mention_text else None
                elif prop.type == "unit_price":
                    line_item.unit_price = float(prop.mention_text) if prop.mention_text else None
                elif prop.type == "line_item_amount":
                    line_item.total_price = float(prop.mention_text) if prop.mention_text else None
            invoice.line_items.append(line_item)
            
    return invoice
