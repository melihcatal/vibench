def normalize_fields(fields):
    return {str(key).lower(): ("" if value is None else str(value).strip()) for key, value in fields.items()}


def build_summary_record(kind, fields, confidence=None):
    record = {"kind": kind, "fields": normalize_fields(fields)}
    if confidence is not None:
        record["confidence"] = confidence
    return record


def required_field_names(document_type):
    if document_type == "invoice":
        return ["vendor", "date", "total"]
    if document_type == "receipt":
        return ["merchant", "tax", "total"]
    return []
