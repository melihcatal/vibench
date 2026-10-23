from typing import Optional, List
from database_client import get_collection, DatabaseClient
from database_models import (
    QueryRequest,
    DocumentResponse,
    to_document_response,
    build_query_filter,
)


@DatabaseClient.handle_mongo_error
def query_documents(
    collection_name: str,
    field_name: str,
    field_value,
    partition_key: Optional[str] = None,
    limit: int = 100,
    sort_field: Optional[str] = None,
    sort_order: int = 1,
    connection_string: Optional[str] = None,
    db_name: Optional[str] = None,
) -> List[DocumentResponse]:
    request = QueryRequest(
        collection=collection_name,
        field_name=field_name,
        field_value=field_value,
        partition_key=partition_key,
        limit=limit,
        sort_field=sort_field,
        sort_order=sort_order,
    )
    collection = get_collection(
        collection_name, connection_string=connection_string, db_name=db_name
    )
    query_filter = build_query_filter(request)
    cursor = collection.find(query_filter).limit(request.limit)
    if request.sort_field:
        cursor = cursor.sort(request.sort_field, request.sort_order)
    results = []
    for raw_doc in cursor:
        results.append(to_document_response(raw_doc, collection_name))
    return results


if __name__ == "__main__":
    docs = query_documents(
        collection_name="users",
        field_name="role",
        field_value="admin",
        partition_key="users",
        limit=50,
    )
    for doc in docs:
        print(doc)
