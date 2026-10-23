import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_models import InvoiceExtraction, LineItem


def extract_invoice_fields(document_bytes: bytes) -> InvoiceExtraction:
    endpoint = os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        "https://your-resource.cognitiveservices.azure.com/",
    )
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
    credential = AzureKeyCredential(key)
    client = DocumentAnalysisClient(endpoint=endpoint, credential=credential)

    poller = client.begin_analyze_document("prebuilt-invoice", document_bytes)
    result = poller.result()

    invoices = result.documents
    if not invoices:
        raise ValueError("No invoice data found in the document")

    invoice = invoices[0]
    fields = invoice.fields

    vendor_name = fields.get("VendorName", {}).get("value", "")
    invoice_date = fields.get("InvoiceDate", {}).get("value", "")
    invoice_number = fields.get("InvoiceId", {}).get("value", "")
    total_amount = fields.get("InvoiceTotal", {}).get("value", 0.0)
    tax_amount = fields.get("TotalTax", {}).get("value", 0.0)
    currency = fields.get("CurrencyCode", {}).get("value", "USD")

    confidence_scores = {}
    for field_name in [
        "VendorName",
        "InvoiceDate",
        "InvoiceId",
        "InvoiceTotal",
        "TotalTax",
        "CurrencyCode",
    ]:
        f = fields.get(field_name)
        if f and f.confidence is not None:
            confidence_scores[field_name] = f.confidence

    line_items = []
    items_field = fields.get("Items", {})
    if items_field and items_field.get("value"):
        for item in items_field["value"]:
            item_fields = item.get("value", {})
            line_items.append(
                LineItem(
                    description=item_fields.get("Description", {}).get("value", ""),
                    quantity=item_fields.get("Quantity", {}).get("value", 0.0),
                    unit_price=item_fields.get("UnitPrice", {}).get("value", 0.0),
                    amount=item_fields.get("Amount", {}).get("value", 0.0),
                )
            )

    return InvoiceExtraction(
        vendor_name=vendor_name,
        invoice_date=str(invoice_date) if invoice_date else "",
        invoice_number=invoice_number,
        total_amount=float(total_amount) if total_amount else 0.0,
        tax_amount=float(tax_amount) if tax_amount else 0.0,
        currency=currency,
        line_items=line_items,
        confidence_scores=confidence_scores,
    )
