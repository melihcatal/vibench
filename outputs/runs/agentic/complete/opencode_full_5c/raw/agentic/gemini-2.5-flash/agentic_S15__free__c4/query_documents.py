from google.cloud import firestore
from database_client import get_db_client
from database_models import Document, QueryFilter


def query_documents(collection_name: str, query_filter: QueryFilter) -> list[Document]:
    """Queries documents by a field value or partition-style key from Firestore."""
    db = get_db_client()
    docs = (
        db.collection(collection_name)
        .where(query_filter.field, "==", query_filter.value)
        .stream()
    )
    return [Document(id=doc.id, data=doc.to_dict()) for doc in docs]
