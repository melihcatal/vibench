from database_models import normalize_item


def record_summary(record):
    item = normalize_item(record) or {}
    text = item.get("title") or item.get("name") or item.get("document_id") or "record"
    return {"summary": str(text)[:120], "fields": list(item.keys())}
