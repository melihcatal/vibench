import os
import base64
from google.cloud import documentai_v1beta3 as documentai
from document_client import get_documentai_client
from document_models import DocumentInput, InvoiceFields

def extract_invoice_fields(document_input: DocumentInput) -> InvoiceFields:
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "us") # e.g., us
    processor_id = os.getenv("GCP_DOCAI_INVOICE_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError("Missing GCP environment variables for Document AI: GCP_PROJECT_ID, GCP_LOCATION, GCP_DOCAI_INVOICE_PROCESSOR_ID")

    client = get_documentai_client()

    # The full resource name of the processor
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    image_content = base64.b64decode(document_input.base64_image)

    # Configure the process request
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type=document_input.mime_type  # e.g., "application/pdf" or "image/jpeg"
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    vendor_name = ""
    invoice_date = ""
    total_amount = 0.0
    currency = ""
    line_items = []

    for entity in document.entities:
        if entity.type == "vendor_name":
            vendor_name = entity.mention_text
        elif entity.type == "invoice_date":
            invoice_date = entity.mention_text
        elif entity.type == "total_amount":
            total_amount = float(entity.mention_text) if entity.mention_text else 0.0
            currency = entity.normalized_value.currency_symbol or entity.normalized_value.currency_code
        elif entity.type == "line_item":
            item_description = ""
            item_quantity = 0
            item_price = 0.0
            item_total = 0.0
            for prop in entity.properties:
                if prop.type == "description":
                    item_description = prop.mention_text
                elif prop.type == "quantity":
                    item_quantity = int(float(prop.mention_text)) if prop.mention_text else 0
                elif prop.type == "unit_price":
                    item_price = float(prop.mention_text) if prop.mention_text else 0.0
                elif prop.type == "amount":
                    item_total = float(prop.mention_text) if prop.mention_text else 0.0
            line_items.append({"description": item_description, "quantity": item_quantity, "unit_price": item_price, "total": item_total})

    return InvoiceFields(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        total_amount=total_amount,
        currency=currency,
        line_items=line_items
    )
