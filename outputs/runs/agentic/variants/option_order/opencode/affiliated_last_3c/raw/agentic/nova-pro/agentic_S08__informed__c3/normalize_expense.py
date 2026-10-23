def normalize_expense(extracted_fields):
    normalized_fields = {
        "vendor": extracted_fields.get("vendor", ""),
        "date": extracted_fields.get("date", ""),
        "total": extracted_fields.get("total", ""),
        "items": extracted_fields.get("items", []),
    }
    return normalized_fields
