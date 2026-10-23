def normalize_expense(extracted_data):
    normalized_data = {
        "vendor": extracted_data["vendor"],
        "date": extracted_data["date"],
        "total": extracted_data["total"],
        "line_items": extracted_data["line_items"],
    }
    return normalized_data
