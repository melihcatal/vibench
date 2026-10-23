import json


def normalize_document(document):
    if isinstance(document, str):
        document = json.loads(document)
    if not isinstance(document, dict):
        raise TypeError("document")
    return document


def normalize_id(document_id):
    if document_id is None:
        raise ValueError("id")
    return str(document_id)


def build_response(document=None, status="ok", **extra):
    response = {"status": status}
    if document is not None:
        response["document"] = document
    response.update(extra)
    return response
