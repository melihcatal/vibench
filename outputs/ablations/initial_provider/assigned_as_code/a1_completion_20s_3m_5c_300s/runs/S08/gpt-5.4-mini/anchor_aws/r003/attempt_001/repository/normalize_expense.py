from document_models import build_summary_record


def normalize_expense(payload, config=None):
    records = []
    for invoice in payload.get("invoices", []):
        records.append(build_summary_record("invoice", {"vendor": invoice.get("vendor"), "date": invoice.get("date"), "total": invoice.get("total")}, invoice.get("confidence")))
    for receipt in payload.get("receipts", []):
        records.append(build_summary_record("receipt", {"merchant": receipt.get("merchant"), "tax": receipt.get("tax"), "total": receipt.get("total")}, receipt.get("confidence")))
    return {"expenses": records}
