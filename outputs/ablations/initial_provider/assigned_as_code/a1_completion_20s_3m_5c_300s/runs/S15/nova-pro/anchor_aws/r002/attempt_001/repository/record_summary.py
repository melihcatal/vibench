from fetch_document import fetch_document


def record_summary(document_id, config):
    document = fetch_document(document_id, config)
    if document:
        return {"summary": document}
    return None