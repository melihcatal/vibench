from document_client import analyze_document


def extract_receipt_fields(document: bytes):
    result = analyze_document("prebuilt-receipt", document)
    fields = (
        result.get("documents", [{}])[0].get("fields", {})
        if isinstance(result, dict)
        else {}
    )
    return {
        "merchant": fields.get("MerchantName") or fields.get("merchant"),
        "tax": fields.get("TotalTax") or fields.get("tax"),
        "total": fields.get("Total") or fields.get("total"),
        "items": fields.get("Items") or [],
        "raw": result,
    }
