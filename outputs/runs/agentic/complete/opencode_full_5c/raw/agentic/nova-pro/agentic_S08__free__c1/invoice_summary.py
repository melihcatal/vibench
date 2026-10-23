from extract_invoice_fields import extract_invoice_fields


def summarize_invoice(document_path):
    extracted_fields = extract_invoice_fields(document_path)
    summary = {
        "vendor": extracted_fields.get("vendor"),
        "date": extracted_fields.get("date"),
        "total": extracted_fields.get("total"),
        "line_items": extracted_fields.get("line_items"),
    }
    return summary
