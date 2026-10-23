from database_client import get_collection
from database_models import QueryRequest, QueryResponse, to_document_response


def query_documents(request: QueryRequest) -> QueryResponse:
    collection = get_collection()
    query_filter = {request.field_name: request.field_value}
    if request.partition_key:
        query_filter["partition_key"] = request.partition_key

    cursor = collection.find(query_filter).limit(request.limit)
    documents = [to_document_response(doc) for doc in cursor]

    return QueryResponse(
        documents=documents,
        total_count=len(documents),
        success=True,
    )
