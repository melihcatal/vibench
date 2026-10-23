import re


def validate_document_fields(fields):
    required = ["vendor", "date", "total"]
    missing = [
        field
        for field in required
        if not fields.get(field) or not re.search(r"\\S", fields[field])
    ]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    else:
        return True
