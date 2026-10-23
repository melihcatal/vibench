from database_client import get_collection
from database_models import (
    DocumentQueryRequest,
    QueryResponse,
    DocumentResponse,
    normalize_document,
)


def query_documents(request: DocumentQueryRequest) -> QueryResponse:
    collection = get_collection()

    filter_criteria = {request.field_name: request.field_value}
    if request.partition_key:
        filter_criteria["partition_key"] = request.partition_key

    cursor = collection.find(filter_criteria).limit(request.limit + 1)

    if request.sort_field:
        cursor = cursor.sort(request.sort_field, request.sort_order)

    raw_docs = list(cursor)
    has_more = len(raw_docs) > request.limit
    if has_more:
        raw_docs = raw_docs[: request.limit]

    documents = [normalize_document(doc) for doc in raw_docs]

    return QueryResponse(
        documents=documents,
        total_count=len(documents),
        has_more=has_more,
    )
