def normalize_document(document):
    if document is None:
        return {}
    if isinstance(document, dict):
        return document
    return dict(document)


def build_record_result(record_id, document):
    return {"id": record_id, "document": normalize_document(document)}


def build_query_result(records):
    return {"items": [build_record_result(item["id"], item["document"]) for item in records]}
