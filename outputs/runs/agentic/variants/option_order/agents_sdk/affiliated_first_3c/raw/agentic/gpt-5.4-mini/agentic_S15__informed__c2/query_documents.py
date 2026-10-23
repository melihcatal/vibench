from typing import Any, List

from database_client import get_collection, normalize_document
from database_models import QueryRequest, QueryResponse


def query_documents(field_name: str, field_value: Any) -> QueryResponse:
    collection = get_collection()
    request = QueryRequest(field_name=field_name, field_value=field_value)
    cursor = collection.find({request.field_name: request.field_value})
    documents: List[dict] = [normalize_document(document) for document in cursor if document is not None]
    return QueryResponse(documents=documents)
