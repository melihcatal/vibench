from database_models import DocumentResponse, normalize_document


def summarize_record(record):
    doc = normalize_document(record) or {}
    text = doc.get("text") or doc.get("description") or ""
    summary = text[:120]
    return DocumentResponse(
        ok=True, data={"summary": summary, "document_id": doc.get("document_id")}
    ).__dict__


def handler(event, context=None):
    return summarize_record(event.get("record", event))
