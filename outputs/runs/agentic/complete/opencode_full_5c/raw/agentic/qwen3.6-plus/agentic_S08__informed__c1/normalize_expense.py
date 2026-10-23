from document_models import (
    InvoiceFields,
    ReceiptFields,
    ExpenseRecord,
    normalize_to_expense_record,
    expense_record_to_dict,
)
from datetime import datetime


def normalize_expense(fields: object, document_type: str, source_id: str = "") -> dict:
    if not isinstance(fields, (InvoiceFields, ReceiptFields)):
        raise ValueError(
            f"Expected InvoiceFields or ReceiptFields, got {type(fields).__name__}"
        )

    record = normalize_to_expense_record(fields, document_type, source_id)

    if record.total <= 0 and record.tax < 0:
        raise ValueError("Invalid expense amounts: total must be positive")

    if not record.date:
        record.date = datetime.utcnow().strftime("%Y-%m-%d")

    if not record.currency:
        record.currency = "USD"

    normalized_items = []
    for item in record.line_items:
        normalized_item = {
            "description": item.get("description", "").strip(),
            "quantity": round(float(item.get("quantity", 0.0)), 2),
            "unit_price": round(float(item.get("unit_price", 0.0)), 2),
            "total_price": round(float(item.get("total_price", 0.0)), 2),
        }
        if normalized_item["description"]:
            normalized_items.append(normalized_item)
    record.line_items = normalized_items

    record.vendor = record.vendor.strip() if record.vendor else "Unknown Vendor"
    record.notes = record.notes.strip() if record.notes else ""

    return expense_record_to_dict(record)


if __name__ == "__main__":
    from document_models import InvoiceFields, LineItem

    sample_fields = InvoiceFields(
        vendor_name="Acme Supplies Inc.",
        invoice_number="INV-2024-001",
        invoice_date="2024-01-15",
        subtotal=100.0,
        tax=8.5,
        total=108.5,
        currency="USD",
        line_items=[
            LineItem(
                description="Office Paper",
                quantity=5,
                unit_price=10.0,
                total_price=50.0,
            ),
            LineItem(
                description="Printer Ink", quantity=2, unit_price=25.0, total_price=50.0
            ),
        ],
    )

    result = normalize_expense(sample_fields, "invoice", "doc-123")
    print(result)
