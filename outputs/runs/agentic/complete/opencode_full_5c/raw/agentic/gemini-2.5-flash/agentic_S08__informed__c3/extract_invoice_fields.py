import os
from typing import List
from google.cloud import documentai_v1 as documentai
from document_models import InvoiceExtractionResult, LineItem
from document_client import (
    get_documentai_client,
    get_gcp_project_id,
    get_documentai_processor_id,
)


def extract_invoice_fields(file_content: bytes) -> InvoiceExtractionResult:
    client = get_documentai_client()

    project_id = get_gcp_project_id()
    processor_id = get_documentai_processor_id()
    location = "us"  # Refer to processor's location information
    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=file_content,
        mime_type="application/pdf",  # Assuming PDF for invoices
    )

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    vendor_name = None
    invoice_date = None
    total_amount = None
    currency = None
    invoice_id = None
    line_items: List[LineItem] = []

    for entity in document.entities:
        if entity.type == "vendor_name" and entity.mention_text:
            vendor_name = entity.mention_text
        elif (
            entity.type == "invoice_date"
            and entity.normalized_value
            and entity.normalized_value.text
        ):
            invoice_date = entity.normalized_value.text
        elif (
            entity.type == "total_amount"
            and entity.normalized_value
            and entity.normalized_value.currency_value
        ):
            total_amount = entity.normalized_value.currency_value.amount
            currency = entity.normalized_value.currency_value.currency
        elif entity.type == "invoice_id" and entity.mention_text:
            invoice_id = entity.mention_text
        elif entity.type == "line_item" and entity.properties:
            description = None
            quantity = None
            unit_price = None
            amount = None
            for prop in entity.properties:
                if prop.type == "description" and prop.mention_text:
                    description = prop.mention_text
                elif (
                    prop.type == "quantity"
                    and prop.normalized_value
                    and prop.normalized_value.text
                ):
                    try:
                        quantity = float(prop.normalized_value.text)
                    except ValueError:
                        pass
                elif (
                    prop.type == "unit_price"
                    and prop.normalized_value
                    and prop.normalized_value.currency_value
                ):
                    unit_price = prop.normalized_value.currency_value.amount
                elif (
                    prop.type == "amount"
                    and prop.normalized_value
                    and prop.normalized_value.currency_value
                ):
                    amount = prop.normalized_value.currency_value.amount
            if description or quantity or unit_price or amount:
                line_items.append(
                    LineItem(
                        description=description if description else "",
                        quantity=quantity,
                        unit_price=unit_price,
                        amount=amount,
                    )
                )

    return InvoiceExtractionResult(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        total_amount=total_amount,
        currency=currency,
        invoice_id=invoice_id,
        line_items=line_items,
        raw_response=document.to_dict(),
    )
