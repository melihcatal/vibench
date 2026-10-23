import datetime

def normalize_document(doc_id: str, data: dict, version: int = 0) -> dict:
    return {
        '_id': doc_id,
        'data': data,
        'version': version,
        'updated_at': datetime.datetime.utcnow()
    }