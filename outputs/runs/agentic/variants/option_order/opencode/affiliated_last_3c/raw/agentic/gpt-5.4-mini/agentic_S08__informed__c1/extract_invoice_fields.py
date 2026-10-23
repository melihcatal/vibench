from document_client import analyze_document


def extract_invoice_fields(document: bytes):
    result = analyze_document("prebuilt-invoice", document)
    fields = (
        result.get("documents", [{}])[0].get("fields", {})
        if isinstance(result, dict)
        else {}
    )
    return {
        "vendor": fields.get("VendorName") or fields.get("vendor"),
        "date": fields.get("InvoiceDate") or fields.get("date"),
        "total": fields.get("InvoiceTotal") or fields.get("total"),
        "line_items": fields.get("Items") or fields.get("line_items", []),
        "raw": result,
    }
