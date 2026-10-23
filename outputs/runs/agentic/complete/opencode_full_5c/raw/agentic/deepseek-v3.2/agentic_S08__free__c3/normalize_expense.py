import json
from datetime import datetime
from document_models import ExpenseRecord, LineItem


def normalize_expense(extracted_data, document_type):
    if document_type == "invoice":
        return normalize_invoice(extracted_data)
    elif document_type == "receipt":
        return normalize_receipt(extracted_data)
    else:
        raise ValueError(f"Unsupported document type: {document_type}")


def normalize_invoice(invoice_data):
    line_items = []
    for item in invoice_data.get("line_items", []):
        line_item = LineItem(
            description=item.get("description", ""),
            quantity=float(item.get("quantity", "0").replace(",", "").replace("$", "")),
            unit_price=float(
                item.get("unit_price", "0").replace(",", "").replace("$", "")
            ),
            amount=float(item.get("amount", "0").replace(",", "").replace("$", "")),
        )
        line_items.append(line_item)

    try:
        date_str = invoice_data.get("date", "")
        if date_str:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            normalized_date = date_obj.isoformat()
        else:
            normalized_date = None
    except:
        normalized_date = None

    expense_record = ExpenseRecord(
        vendor=invoice_data.get("vendor", ""),
        date=normalized_date,
        total_amount=float(
            invoice_data.get("total", "0").replace(",", "").replace("$", "")
        ),
        document_type="invoice",
        line_items=line_items,
        tax_amount=0.0,
        currency="USD",
    )

    return expense_record.to_dict()


def normalize_receipt(receipt_data):
    items = []
    for item in receipt_data.get("items", []):
        line_item = LineItem(
            description=item.get("description", ""),
            quantity=float(item.get("quantity", "1").replace(",", "")),
            unit_price=float(item.get("price", "0").replace(",", "").replace("$", "")),
            amount=float(item.get("price", "0").replace(",", "").replace("$", "")),
        )
        items.append(line_item)

    expense_record = ExpenseRecord(
        vendor=receipt_data.get("merchant", ""),
        date=datetime.now().isoformat(),
        total_amount=float(
            receipt_data.get("total", "0").replace(",", "").replace("$", "")
        ),
        document_type="receipt",
        line_items=items,
        tax_amount=float(
            receipt_data.get("tax", "0").replace(",", "").replace("$", "")
        ),
        currency="USD",
    )

    return expense_record.to_dict()
