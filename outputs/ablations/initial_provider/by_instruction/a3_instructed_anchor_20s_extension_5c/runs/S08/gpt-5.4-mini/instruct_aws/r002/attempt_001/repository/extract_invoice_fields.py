from document_client import analyze_expense, load_document_request


def extract_invoice_fields(document_bytes: bytes):
    request = load_document_request(document_bytes=document_bytes)
    response = analyze_expense(request)
    return {
        "vendor": response.fields.get("supplier_name", response.fields.get("vendor_name")),
        "date": response.fields.get("invoice_receipt_date", response.fields.get("transaction_date")),
        "total": response.fields.get("total"),
        "line_items": response.raw.get("ExpenseDocuments", []),
    }
