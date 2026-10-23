from database_client import coll
from database_models import prepare_document

def upsert_document(doc_id: str, document: dict) -> bool:
    doc = prepare_document(doc_id, document)
    result = coll.replace_one({"_id": doc_id}, doc, upsert=True)
    return result.acknowledged