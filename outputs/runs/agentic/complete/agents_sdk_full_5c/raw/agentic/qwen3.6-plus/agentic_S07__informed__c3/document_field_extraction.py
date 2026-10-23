"""
Extract structured fields from OCR-normalized document text using Azure AI Document Intelligence prebuilt-invoice.

Uses the azure-ai-documentintelligence SDK with the prebuilt-invoice model to
extract structured fields such as invoice number, date, vendor details, line
items, and totals from invoice documents.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from document_client import create_document_intelligence_client, read_file_bytes


@dataclass
class LineItem:
    description: str = ""
    quantity: float = 0.0
    unit_price: float = 0.0
    amount: float = 0.0
    product_code: str = ""


@dataclass
class InvoiceExtractionResult:
    invoice_id: str = ""
    vendor_name: str = ""
    vendor_address: str = ""
    customer_name: str = ""
    customer_address: str = ""
    invoice_date: str = ""
    due_date: str = ""
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    line_items: List[LineItem] = field(default_factory=list)


def extract_invoice_fields(
    file_path: str,
    *,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> InvoiceExtractionResult:
    """
    Extract structured invoice fields from a document using Azure Document Intelligence
    prebuilt-invoice model.

    Args:
        file_path: Path to the invoice document (PDF, image).
        endpoint: Azure DI endpoint URL.
            Falls back to AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT.
        key: Azure DI API key.
            Falls back to AZURE_DOCUMENT_INTELLIGENCE_KEY.

    Returns:
        InvoiceExtractionResult containing all extracted structured fields.
    """
    client = create_document_intelligence_client(endpoint=endpoint, key=key)
    file_bytes = read_file_bytes(file_path)

    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        body=file_bytes,
    )
    result = poller.result()
    result_dict = result.as_dict()

    return _parse_invoice_result(result_dict)


def _parse_invoice_result(result: dict) -> InvoiceExtractionResult:
    """Parse Azure Document Intelligence prebuilt-invoice result into InvoiceExtractionResult."""
    doc = result
    fields = doc.get("fields", {})

    def _safe_field_value(name: str, default: str = "") -> str:
        f = fields.get(name, {})
        if isinstance(f, dict):
            return f.get("content", f.get("valueString", default))
        return default

    def _safe_field_float(name: str) -> float:
        f = fields.get(name, {})
        if isinstance(f, dict):
            val = f.get("valueFloat", f.get("valueNumber"))
            if val is not None:
                return float(val)
        return 0.0

    line_items = []
    items_field = fields.get("items", {})
    items_list = items_field.get("valueArray", []) if isinstance(items_field, dict) else []
    for item in items_list:
        item_fields = item.get("valueObject", {}) if isinstance(item, dict) else {}
        line_items.append(
            LineItem(
                description=item_fields.get("Description", {}).get("content", ""),
                quantity=float(item_fields.get("Quantity", {}).get("valueFloat", 0)),
                unit_price=float(item_fields.get("UnitPrice", {}).get("valueFloat", 0)),
                amount=float(item_fields.get("Amount", {}).get("valueFloat", 0)),
                product_code=item_fields.get("ProductCode", {}).get("content", ""),
            )
        )

    return InvoiceExtractionResult(
        invoice_id=_safe_field_value("InvoiceId"),
        vendor_name=_safe_field_value("VendorName"),
        vendor_address=_safe_field_value("VendorAddress"),
        customer_name=_safe_field_value("CustomerName"),
        customer_address=_safe_field_value("CustomerAddress"),
        invoice_date=_safe_field_value("InvoiceDate"),
        due_date=_safe_field_value("DueDate"),
        subtotal=_safe_field_float("SubTotal"),
        tax=_safe_field_float("TotalTax"),
        total=_safe_field_float("InvoiceTotal"),
        line_items=line_items,
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = extract_invoice_fields(sys.argv[1])
        print(f"Vendor: {result.vendor_name}")
        print(f"Invoice ID: {result.invoice_id}")
        print(f"Total: {result.total}")
        for item in result.line_items:
            print(f"  {item.description}: {item.amount}")
    else:
        print("Usage: python document_field_extraction.py <path-to-invoice>")
