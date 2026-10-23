from document_client import DocumentClient
from document_models import InvoiceFields, LineItem
from azure.ai.documentintelligence.models import DocumentAnalysisFeature, ContentFormat
from typing import Dict, Any, List, Optional

def extract_invoice_fields(document_path: str) -> InvoiceFields:
    doc_client = DocumentClient()
    client = doc_client.get_client()

    with open(document_path, "rb") as f: # type: ignore
        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    invoice_fields = InvoiceFields()
    if result.documents and len(result.documents) > 0:
        invoice = result.documents[0]
        if invoice.fields:
            invoice_fields.vendor_name = invoice.fields.get("VendorName")?.value if invoice.fields.get("VendorName") else None  # type: ignore
            invoice_fields.invoice_date = invoice.fields.get("InvoiceDate")?.value if invoice.fields.get("InvoiceDate") else None # type: ignore
            invoice_fields.invoice_total = invoice.fields.get("InvoiceTotal")?.value if invoice.fields.get("InvoiceTotal") else None # type: ignore
            
            if invoice.fields.get("Items"):
                for item in invoice.fields["Items"].value:
                    line_item = LineItem(
                        description=item.value.get("Description")?.value if item.value.get("Description") else None, # type: ignore
                        quantity=item.value.get("Quantity")?.value if item.value.get("Quantity") else None, # type: ignore
                        unit_price=item.value.get("UnitPrice")?.value if item.value.get("UnitPrice") else None, # type: ignore
                        amount=item.value.get("Amount")?.value if item.value.get("Amount") else None # type: ignore
                    )
                    invoice_fields.line_items.append(line_item)

    return invoice_fields
