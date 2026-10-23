from database_client import get_collection
from database_models import (
    DocumentQueryRequest,
    DocumentQueryResponse,
    DocumentFetchResponse,
)


def query_documents(request: DocumentQueryRequest) -> DocumentQueryResponse:
    collection = get_collection()
    mongo_filter = request.to_mongo_filter()

    cursor = collection.find(mongo_filter).limit(request.limit)
    if request.sort_field:
        cursor = cursor.sort(f"data.{request.sort_field}", request.sort_order)

    docs = list(cursor)
    fetched = [DocumentFetchResponse.from_mongo_document(d) for d in docs]
    total = collection.count_documents(mongo_filter)

    return DocumentQueryResponse(
        documents=fetched,
        total_count=total,
        limit=request.limit,
    )


def query_documents_raw(
    field_name: str, field_value, partition_key: str = None, limit: int = 50
) -> dict:
    request = DocumentQueryRequest(
        field_name=field_name,
        field_value=field_value,
        partition_key=partition_key,
        limit=limit,
    )
    response = query_documents(request)
    return response.to_dict()


if __name__ == "__main__":
    result = query_documents_raw(
        field_name="status", field_value="active", partition_key="default", limit=10
    )
    print(result)
