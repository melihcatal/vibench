def normalize_document(document):
    return dict(document or {})


def normalize_payload(payload):
    payload = dict(payload or {})
    if "document" in payload and payload["document"] is not None:
        payload["document"] = normalize_document(payload["document"])
    return payload


def build_response(id=None, document=None, documents=None, updated=None, archived=None):
    response = {}
    if id is not None:
        response["id"] = id
    if document is not None:
        response["document"] = normalize_document(document)
    if documents is not None:
        response["documents"] = [normalize_document(item) for item in documents]
    if updated is not None:
        response["updated"] = updated
    if archived is not None:
        response["archived"] = archived
    return response
