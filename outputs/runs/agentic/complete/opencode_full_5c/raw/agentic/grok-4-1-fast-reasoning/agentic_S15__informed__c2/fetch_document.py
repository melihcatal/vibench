from typing import Dict, Any, Optional
from database_client import get_mongodb_client, get_database, get_collection
from database_models import Document


def fetch_document(doc_id: str) -> Optional[Document]:
    client = get_mongodb_client()
    db = get_database(client)
    coll = get_collection(db)
    doc = coll.find_one({"_id": doc_id})
    client.close()
    return doc
