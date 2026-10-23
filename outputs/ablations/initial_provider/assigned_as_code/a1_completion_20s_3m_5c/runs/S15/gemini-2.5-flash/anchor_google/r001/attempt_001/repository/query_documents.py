from database_client import get_firestore_client
from database_models import Document, QueryCondition
from typing import List


def query_documents(condition: QueryCondition) -> List[Document]:
    client = get_firestore_client()
    query = (
        client.collection(r"documents")
        .where(condition.field, condition.operator, condition.value)
        .stream()
    )
    results = []
    for doc in query:
        results.append(Document(id=doc.id, document=doc.to_dict()))
    return results
