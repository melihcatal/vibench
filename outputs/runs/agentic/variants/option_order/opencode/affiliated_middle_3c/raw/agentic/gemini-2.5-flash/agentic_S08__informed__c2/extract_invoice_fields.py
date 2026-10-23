import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import ExtractedInvoice, InvoiceLineItem


def extract_invoice_fields(
    file_content: bytes, project_id: str, location: str, processor_id: str
) -> ExtractedInvoice:
    client = get_documentai_client()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    document = documentai.RawDocument(
        content=file_content, mime_type="application/pdf"
    )  # Assuming PDF

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=document)

    result = client.process_document(request=request)
    document_response = result.document

    vendor_name = None
    invoice_date = None
    invoice_total = None
    line_items = []

    for entity in document_response.entities:
        if entity.type == "vendor_name" and entity.mention_text:
            vendor_name = entity.mention_text
        elif entity.type == "invoice_date" and entity.mention_text:
            invoice_date = entity.mention_text
        elif entity.type == "total_amount" and entity.mention_text:
            try:
                invoice_total = float(entity.mention_text)
            except ValueError:
                pass
        elif entity.type == "line_item":
            item_description = None
            item_quantity = None
            item_unit_price = None
            item_total_price = None
            for prop in entity.properties:
                if prop.type == "description" and prop.mention_text:
                    item_description = prop.mention_text
                elif prop.type == "quantity" and prop.mention_text:
                    try:
                        item_quantity = float(prop.mention_text)
                    except ValueError:
                        pass
                elif prop.type == "unit_price" and prop.mention_text:
                    try:
                        item_unit_price = float(prop.mention_text)
                    except ValueError:
                        pass
                elif prop.type == "amount" and prop.mention_text:
                    try:
                        item_total_price = float(prop.mention_text)
                    except ValueError:
                        pass
            if item_description:
                line_items.append(
                    InvoiceLineItem(
                        description=item_description,
                        quantity=item_quantity,
                        unit_price=item_unit_price,
                        total_price=item_total_price,
                    )
                )

    return ExtractedInvoice(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        invoice_total=invoice_total,
        line_items=line_items,
    )
