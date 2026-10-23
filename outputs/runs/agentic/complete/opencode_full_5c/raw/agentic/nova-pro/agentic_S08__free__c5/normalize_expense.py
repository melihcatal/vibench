def normalize_expense(extracted_fields):
    normalized_expense = {
        "vendor": extracted_fields.get("vendor", ""),
        "date": extracted_fields.get("date", ""),
        "total": extracted_fields.get("total", ""),
        "line_items": extracted_fields.get("line_items", []),
    }
    return normalized_expense
