import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
from document_client import get_documentai_client
from document_models import ExtractedInvoiceFields, InvoiceLineItem
from typing import Any

def extract_invoice_fields_docai(file_content: bytes, mime_type: str = "application/pdf") -> ExtractedInvoiceFields:
    """
    Extracts invoice fields using Google Cloud Document AI.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    Requires GCP_DOCAI_PROJECT_ID and GCP_DOCAI_INVOICE_PROCESSOR_ID environment variables.
    """
    project_id = os.getenv("GCP_DOCAI_PROJECT_ID")
    processor_id = os.getenv("GCP_DOCAI_INVOICE_PROCESSOR_ID")
    location = os.getenv("GCP_DOCAI_LOCATION", "us") # e.g., 'us' or 'eu'

    if not project_id or not processor_id:
        raise ValueError("GCP_DOCAI_PROJECT_ID and GCP_DOCAI_INVOICE_PROCESSOR_ID must be set.")

    client = get_documentai_client()
    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    vendor_name = None
    invoice_date = None
    total_amount = None
    currency = None
    line_items_data = []

    for entity in document.entities:
        if entity.type_ == "supplier_name" and entity.mention_text:
            vendor_name = entity.mention_text
        elif entity.type_ == "invoice_date" and entity.mention_text:
            invoice_date = entity.mention_text
        elif entity.type_ == "total_amount" and entity.mention_text:
            try:
                total_amount = float(entity.mention_text)
                if entity.currency_text:
                    currency = entity.currency_text
            except ValueError:
                pass
        elif entity.type_ == "line_item":
            item = InvoiceLineItem()
            for prop in entity.properties:
                if prop.type_ == "description" and prop.mention_text:
                    item.description = prop.mention_text
                elif prop.type_ == "quantity" and prop.mention_text:
                    try:
                        item.quantity = float(prop.mention_text)
                    except ValueError:
                        pass
                elif prop.type_ == "unit_price" and prop.mention_text:
                    try:
                        item.unit_price = float(prop.mention_text)
                    except ValueError:
                        pass
                elif prop.type_ == "amount" and prop.mention_text:
                    try:
                        item.amount = float(prop.mention_text)
                    except ValueError:
                        pass
            if item.description or item.quantity or item.unit_price or item.amount:
                line_items_data.append(item)

    return ExtractedInvoiceFields(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        total_amount=total_amount,
        currency=currency,
        line_items=line_items_data,
        raw_text=document.text
    )
