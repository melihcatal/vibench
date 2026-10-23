from typing import Any, List
from database_client import get_mongo_client, get_database, get_documents_collection
from database_models import Document


def query_documents(field: str, value: Any) -> List[Document]:
    client = get_mongo_client()
    db = get_database(client)
    collection = get_documents_collection(db)
    return list(collection.find({field: value}))
