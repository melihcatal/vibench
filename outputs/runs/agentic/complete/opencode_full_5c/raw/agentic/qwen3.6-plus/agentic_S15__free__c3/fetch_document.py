from typing import Optional
from database_client import get_collection, DatabaseClient
from database_models import DocumentResponse, to_document_response


@DatabaseClient.handle_mongo_error
def fetch_document(
    collection_name: str,
    document_id: str,
    partition_key: Optional[str] = None,
    connection_string: Optional[str] = None,
    db_name: Optional[str] = None,
) -> Optional[DocumentResponse]:
    collection = get_collection(
        collection_name, connection_string=connection_string, db_name=db_name
    )
    query_filter = {"_id": document_id}
    if partition_key:
        query_filter["partition_key"] = partition_key
    raw_doc = collection.find_one(query_filter)
    if raw_doc is None:
        return None
    return to_document_response(raw_doc, collection_name)


if __name__ == "__main__":
    doc = fetch_document(
        collection_name="users", document_id="user_001", partition_key="users"
    )
    print(doc)
