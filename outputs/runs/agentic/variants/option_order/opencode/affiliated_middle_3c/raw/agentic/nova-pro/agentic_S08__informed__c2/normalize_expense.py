def normalize_expense(extracted_data):
    normalized_data = {
        "vendor": extracted_data.get("vendor", ""),
        "date": extracted_data.get("date", ""),
        "total": extracted_data.get("total", ""),
        "line_items": extracted_data.get("line_items", []),
    }
    return normalized_data
