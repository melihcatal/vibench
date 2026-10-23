from decimal import Decimal


def normalize_document(document):
    if document:
        return json.loads(json.dumps(document), parse_float=Decimal)
    return None


def normalize_documents(documents):
    return [normalize_document(doc) for doc in documents]