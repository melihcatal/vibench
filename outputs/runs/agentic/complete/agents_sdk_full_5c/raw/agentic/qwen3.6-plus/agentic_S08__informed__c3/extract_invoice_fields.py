"""Extract vendor, date, total, and line-item fields from an invoice using Azure Document Intelligence."""

import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_models import InvoiceExtractionResult, LineItem
from document_client import get_document_intelligence_client


def extract_invoice_fields(document_path: str) -> InvoiceExtractionResult:
    """Extract structured fields from an invoice document.

    Uses Azure Document Intelligence prebuilt-invoice model (model ID: prebuilt-invoice).
    Returns vendor name, invoice date, total amount, and line items.
    """
    endpoint = os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        "https://<your-resource>.cognitiveservices.azure.com/"
    )
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

    client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-invoice",
            body=f
        )
        result = poller.result()

    invoices = result.documents
    if not invoices:
        return InvoiceExtractionResult(
            vendor_name="",
            invoice_date="",
            total_amount=0.0,
            line_items=[],
            confidence=0.0,
            raw_fields={}
        )

    invoice = invoices[0]
    fields = invoice.fields

    vendor_name = ""
    vendor_confidence = 0.0
    if "VendorName" in fields:
        vendor_name_field = fields["VendorName"]
        vendor_name = vendor_name_field.value or ""
        vendor_confidence = vendor_name_field.confidence or 0.0

    invoice_date = ""
    date_confidence = 0.0
    if "InvoiceDate" in fields:
        date_field = fields["InvoiceDate"]
        invoice_date = str(date_field.value) if date_field.value else ""
        date_confidence = date_field.confidence or 0.0

    total_amount = 0.0
    total_confidence = 0.0
    if "InvoiceTotal" in fields:
        total_field = fields["InvoiceTotal"]
        total_amount = float(total_field.value) if total_field.value else 0.0
        total_confidence = total_field.confidence or 0.0

    line_items = []
    items_confidence = 0.0
    if "Items" in fields:
        items_field = fields["Items"]
        if items_field.value:
            for idx, item in enumerate(items_field.value):
                description = ""
                quantity = 0.0
                unit_price = 0.0
                amount = 0.0

                if "Description" in item.value:
                    desc_field = item.value["Description"]
                    description = desc_field.value or ""

                if "Quantity" in item.value:
                    qty_field = item.value["Quantity"]
                    quantity = float(qty_field.value) if qty_field.value else 0.0

                if "UnitPrice" in item.value:
                    price_field = item.value["UnitPrice"]
                    unit_price = float(price_field.value) if price_field.value else 0.0

                if "Amount" in item.value:
                    amt_field = item.value["Amount"]
                    amount = float(amt_field.value) if amt_field.value else 0.0

                line_items.append(LineItem(
                    description=description,
                    quantity=quantity,
                    unit_price=unit_price,
                    amount=amount
                ))

            if items_field.confidence:
                items_confidence = items_field.confidence

    overall_confidence = sum([
        vendor_confidence,
        date_confidence,
        total_confidence,
        items_confidence
    ]) / 4.0 if any([vendor_confidence, date_confidence, total_confidence, items_confidence]) else 0.0

    raw_fields = {
        "VendorName": vendor_name,
        "InvoiceDate": invoice_date,
        "InvoiceTotal": total_amount,
        "ItemCount": len(line_items)
    }

    return InvoiceExtractionResult(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        total_amount=total_amount,
        line_items=line_items,
        confidence=overall_confidence,
        raw_fields=raw_fields
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = extract_invoice_fields(sys.argv[1])
        print(result.model_dump_json(indent=2))
