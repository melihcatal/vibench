from database_client import get_collection

def fetch_document(doc_id: str) -> dict | None:
    coll = get_collection()
    return coll.find_one({'_id': doc_id})