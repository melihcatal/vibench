from document_client import analyze_expense, load_document_request


def extract_receipt_fields(document_bytes: bytes):
    request = load_document_request(document_bytes=document_bytes)
    response = analyze_expense(request)
    return {
        "merchant": response.fields.get("supplier_name", response.fields.get("merchant_name")),
        "tax": response.fields.get("tax"),
        "total": response.fields.get("total"),
        "items": response.raw.get("ExpenseDocuments", []),
    }
