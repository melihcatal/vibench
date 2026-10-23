import os
from typing import Dict, Any, List
from google.cloud import documentai_v1 as documentai
from document_client import DocumentClients, PROJECT_ID, LOCATION, INVOICE_PROCESSOR_ID
from document_models import Invoice, LineItem
import datetime

def extract_invoice_fields(document_bytes: bytes, document_id: str = None) -> Invoice:
    """Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.

    Args:
        document_bytes: The content of the document as bytes.
        document_id: Optional unique identifier for the document.

    Returns:
        An Invoice dataclass instance.
    """
    client = DocumentClients.get_documentai_client()

    # The Document AI project ID and processor ID are configured in document_client.py
    name = INVOICE_PROCESSOR_ID

    # Read the document content
    raw_document = documentai.RawDocument(
        content=document_bytes,
        mime_type="application/pdf" # Assuming PDF for invoices
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document
    )

    # Process the document
    response = client.process_document(request=request)
    document = response.document

    # --- Extract fields from Document AI output ---
    vendor_name = None
    invoice_date = None
    total_amount = None
    currency = None
    line_items: List[LineItem] = []

    for entity in document.entities:
        if entity.type == "supplier_name" and entity.mention_text:
            vendor_name = entity.mention_text
        elif entity.type == "invoice_date" and entity.mention_text:
            try:
                invoice_date = datetime.datetime.strptime(entity.mention_text, "%Y-%m-%d").date() # Assuming YYYY-MM-DD
            except ValueError:
                # Attempt other formats or log error
                pass
        elif entity.type == "total_amount" and entity.mention_text:
            try:
                total_amount = float(entity.mention_text.replace('$', '').replace(',', '')) # Basic cleaning
                if entity.properties and entity.properties[0].type == "currency" and entity.properties[0].mention_text:
                    currency = entity.properties[0].mention_text
            except ValueError:
                pass
        elif entity.type == "line_item" and entity.properties:
            item_description = None
            item_quantity = None
            item_unit_price = None
            item_total_amount = None

            for prop in entity.properties:
                if prop.type == "description" and prop.mention_text:
                    item_description = prop.mention_text
                elif prop.type == "quantity" and prop.mention_text:
                    try: item_quantity = float(prop.mention_text) # Simplified
                    except ValueError: pass
                elif prop.type == "unit_price" and prop.mention_text:
                    try: item_unit_price = float(prop.mention_text.replace('$', '').replace(',', ''))
                    except ValueError: pass
                elif prop.type == "amount" and prop.mention_text:
                    try: item_total_amount = float(prop.mention_text.replace('$', '').replace(',', ''))
                    except ValueError: pass

            line_items.append(LineItem(
                description=item_description,
                quantity=item_quantity,
                unit_price=item_unit_price,
                total_amount=item_total_amount
            ))

    return Invoice(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        total_amount=total_amount,
        currency=currency,
        line_items=line_items,
        raw_document_url="", # In a real scenario, this would be a GCS URL
        document_id=document_id
    )
