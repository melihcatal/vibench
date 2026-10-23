from database_client import coll
from database_models import parse_document

def fetch_document(doc_id: str) -> Optional[dict]:
    raw_doc = coll.find_one({"_id": doc_id})
    return parse_document(raw_doc)