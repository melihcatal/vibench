from typing import Optional
from database_client import get_mongo_client, get_database, get_documents_collection
from database_models import Document


def fetch_document(doc_id: str) -> Optional[Document]:
    client = get_mongo_client()
    db = get_database(client)
    collection = get_documents_collection(db)
    return collection.find_one({"doc_id": doc_id})
