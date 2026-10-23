import os

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_azure_document_intelligence_client, get_document_bytes


def extract_invoice_fields(source):
    client = get_azure_document_intelligence_client()
    poller = client.begin_analyze_document(
        "prebuilt-invoice",
        AnalyzeDocumentRequest(bytes_source=get_document_bytes(source)),
    )
    result = poller.result()
    invoice = result.documents[0].fields if result.documents else {}
    line_items = []
    for item in (
        (invoice.get("Items") or {}).value_array
        if hasattr(invoice.get("Items"), "value_array")
        else []
    ):
        fields = item.value_object
        line_items.append(
            {
                "description": getattr(fields.get("Description"), "content", None),
                "quantity": getattr(fields.get("Quantity"), "content", None),
                "unit_price": getattr(fields.get("UnitPrice"), "content", None),
                "amount": getattr(fields.get("Amount"), "content", None),
            }
        )
    return {
        "vendor": getattr(invoice.get("VendorName"), "content", None),
        "date": getattr(invoice.get("InvoiceDate"), "content", None),
        "total": getattr(invoice.get("InvoiceTotal"), "content", None),
        "tax": getattr(invoice.get("TotalTax"), "content", None),
        "items": line_items,
    }


if __name__ == "__main__":
    path = os.environ.get("DOCUMENT_PATH")
    if path:
        print(extract_invoice_fields(path))
