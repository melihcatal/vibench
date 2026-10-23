import os
from google.cloud import documentai

from document_client import get_google_credentials
from document_models import ParsedInvoice

def extract_invoice_fields(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> ParsedInvoice:
    """
    Processes an invoice document using Google Cloud Document AI.
    """
    credentials = get_google_credentials()
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts, credentials=credentials)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    vendor_name = ""
    invoice_date = ""
    total_amount = ""
    line_items = []

    for entity in document.entities:
        if entity.type_ == "supplier_name":
            vendor_name = entity.mention_text
        elif entity.type_ == "invoice_date":
            invoice_date = entity.mention_text
        elif entity.type_ == "total_amount":
            total_amount = entity.mention_text
        elif entity.type_ == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type_ == "line_item/description":
                    item["description"] = prop.mention_text
                elif prop.type_ == "line_item/amount":
                    item["amount"] = prop.mention_text
            if item:
                line_items.append(item)

    return ParsedInvoice(
        vendor=vendor_name,
        date=invoice_date,
        total=total_amount,
        line_items=line_items,
    )
