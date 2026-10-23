from database_client import get_collection
from database_models import QueryDocumentsRequest


def query_documents(request: QueryDocumentsRequest):
    docs = get_collection(request.collection).where(request.field_name, "==", request.field_value).stream()
    return [doc.to_dict() for doc in docs]
