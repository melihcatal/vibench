import base64
import datetime
from typing import Dict, Any
from google.cloud import documentai_v1beta3 as documentai
from document_client import DocumentClient
from document_models import DocumentExtractionRequest, InvoiceExtractionResult, LineItem


def extract_invoice_fields(
    request: DocumentExtractionRequest,
) -> InvoiceExtractionResult:
    client = DocumentClient()
    processor_name = client.get_documentai_processor_path(
        client.documentai_invoice_processor_id
    )

    # The raw document bytes
    document = documentai.RawDocument(
        content=base64.b64decode(request.document_content),
        mime_type="application/pdf",  # Assuming PDF for invoices
    )

    # Configure the process request
    request_docai = documentai.ProcessRequest(
        name=processor_name, raw_document=document
    )

    # Use the Document AI client to process the document
    response_docai = client.documentai_client.process_document(request_docai)
    document_proto = response_docai.document

    vendor_name = None
    invoice_date = None
    total_amount = None
    currency = None
    line_items = []

    # Extract fields from Document AI response
    for entity in document_proto.entities:
        if entity.type == "supplier_name" and entity.mention_text:
            vendor_name = entity.mention_text
        elif entity.type == "invoice_date" and entity.mention_text:
            try:
                invoice_date = datetime.datetime.strptime(
                    entity.mention_text, "%Y-%m-%d"
                ).date()
            except ValueError:
                pass
        elif entity.type == "total_amount" and entity.mention_text:
            try:
                total_amount = float(entity.mention_text)
                if entity.currency_text:
                    currency = entity.currency_text
            except ValueError:
                pass
        elif entity.type == "line_item":
            item = LineItem()
            for sub_entity in entity.properties:
                if sub_entity.type == "description" and sub_entity.mention_text:
                    item.description = sub_entity.mention_text
                elif sub_entity.type == "quantity" and sub_entity.mention_text:
                    try:
                        item.quantity = float(sub_entity.mention_text)
                    except ValueError:
                        pass
                elif sub_entity.type == "unit_price" and sub_entity.mention_text:
                    try:
                        item.unit_price = float(sub_entity.mention_text)
                    except ValueError:
                        pass
                elif sub_entity.type == "total_amount" and sub_entity.mention_text:
                    try:
                        item.total_price = float(sub_entity.mention_text)
                    except ValueError:
                        pass
            if item.description or item.total_price:
                line_items.append(item)

    return InvoiceExtractionResult(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        total_amount=total_amount,
        currency=currency,
        line_items=line_items,
        raw_response=documentai.Document.to_dict(
            document_proto
        ),  # Convert proto to dict for raw_response
    )
