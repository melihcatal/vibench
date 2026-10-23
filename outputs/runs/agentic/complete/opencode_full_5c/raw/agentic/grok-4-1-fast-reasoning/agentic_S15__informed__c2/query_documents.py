from typing import Dict, Any, List
from database_client import get_mongodb_client, get_database, get_collection
from database_models import Document, QueryFilter


def query_documents(query_filter: QueryFilter) -> List[Document]:
    client = get_mongodb_client()
    db = get_database(client)
    coll = get_collection(db)
    cursor = coll.find(query_filter)
    documents = list(cursor)
    client.close()
    return documents
