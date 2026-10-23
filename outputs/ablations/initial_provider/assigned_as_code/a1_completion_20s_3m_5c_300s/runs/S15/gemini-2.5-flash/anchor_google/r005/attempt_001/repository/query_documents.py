from database_client import get_firestore_client
from database_models import Document, DocumentQuery
from google.cloud.firestore import Client
from typing import List


def query_documents(query: DocumentQuery, client: Client = None, project_id: str = None) -> List[Document]:
    client = client or get_firestore_client(project_id=project_id)
    docs_ref = client.collection(query.collection).where(query.field, "==", query.value).stream()
    results = []
    for doc in docs_ref:
        data = doc.to_dict()
        results.append(Document(id=doc.id, data=data))
    return results
