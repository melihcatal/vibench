from decimal import Decimal


def deserialize_document(item):
    if not item:
        return None
    return {k: v if not isinstance(v, Decimal) else float(v) for k, v in item.items()}


def deserialize_documents(items):
    return [deserialize_document(item) for item in items]