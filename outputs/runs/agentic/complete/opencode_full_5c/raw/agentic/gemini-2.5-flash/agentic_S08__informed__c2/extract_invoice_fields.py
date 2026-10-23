import os
from google.cloud import documentai_v1 as documentai
from document_models import ExtractedInvoice, LineItem
from document_client import get_documentai_client


def extract_invoice_fields(file_content: bytes, mime_type: str) -> ExtractedInvoice:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Document AI.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"  # Or your preferred location
    processor_id = os.environ.get(
        "DOCUMENT_AI_INVOICE_PROCESSOR_ID"
    )  # Specific processor ID for invoice parsing

    if not all([project_id, location, processor_id]):
        raise ValueError(
            "Missing GOOGLE_CLOUD_PROJECT, DOCUMENT_AI_INVOICE_PROCESSOR_ID environment variables."
        )

    processor_name = documentai.DocumentProcessorServiceClient.processor_path(
        project_id, location, processor_id
    )

    document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=document)

    client = get_documentai_client()
    result = client.process_document(request=request)
    document_proto = result.document

    extracted_invoice = ExtractedInvoice(raw_text=document_proto.text)

    for entity in document_proto.entities:
        if entity.type == "vendor_name":
            extracted_invoice.vendor_name = entity.mention_text
        elif entity.type == "invoice_date":
            extracted_invoice.invoice_date = entity.mention_text
        elif entity.type == "total_amount":
            if entity.money_value and entity.money_value.units is not None:
                extracted_invoice.total_amount = float(entity.money_value.units) + (
                    float(entity.money_value.nanos) / 1e9
                    if entity.money_value.nanos
                    else 0
                )
                extracted_invoice.currency = entity.money_value.currency
            elif entity.mention_text:
                try:
                    extracted_invoice.total_amount = float(entity.mention_text)
                except ValueError:
                    pass
        elif entity.type == "line_item":
            line_item = LineItem(description=entity.mention_text)
            for prop in entity.properties:
                if prop.type == "description":
                    line_item.description = prop.mention_text
                elif prop.type == "quantity":
                    if (
                        prop.normalized_value
                        and prop.normalized_value.float_value is not None
                    ):
                        line_item.quantity = prop.normalized_value.float_value
                elif prop.type == "unit_price":
                    if prop.money_value and prop.money_value.units is not None:
                        line_item.unit_price = float(prop.money_value.units) + (
                            float(prop.money_value.nanos) / 1e9
                            if prop.money_value.nanos
                            else 0
                        )
                elif prop.type == "amount":  # Total price for line item
                    if prop.money_value and prop.money_value.units is not None:
                        line_item.total_price = float(prop.money_value.units) + (
                            float(prop.money_value.nanos) / 1e9
                            if prop.money_value.nanos
                            else 0
                        )
            extracted_invoice.line_items.append(line_item)

    return extracted_invoice
