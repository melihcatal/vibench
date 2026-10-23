def _confidence(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def normalize_text_fields(fields):
    return {str(k).lower(): ("" if v is None else str(v)) for k, v in (fields or {}).items()}


def extract_textract_summary(document):
    fields = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in document.get("SummaryFields", [])}
    items = []
    for group in document.get("LineItemGroups", []):
        for item in group.get("LineItems", []):
            values = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in item.get("LineItemExpenseFields", [])}
            items.append(values)
    return fields, items


def field_confidence_map(fields):
    return {str(k): _confidence(v) for k, v in (fields or {}).items()}
