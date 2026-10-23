from database_client import get_firestore_client, get_collection_name
from database_models import Document, QueryFilter
from typing import List, Dict, Any


def query_documents(query_filter: QueryFilter) -> List[Document]:
    db = get_firestore_client()
    collection_ref = db.collection(get_collection_name())

    query = collection_ref.where(query_filter.field, "==", query_filter.value)
    results = query.stream()

    documents = []
    for doc in results:
        data = doc.to_dict()
        version = data.pop("version", None)
        documents.append(Document(id=doc.id, data=data, version=version))
    return documents
