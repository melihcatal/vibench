import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from database_client import get_mongo_client, get_database_name, get_collection_name
from database_models import QueryRequest, QueryResponse, QueryResultItem


def query_documents(
    field: str, value: str, partition_key: str | None = None, limit: int = 50
) -> QueryResponse:
    client = get_mongo_client()
    db_name = get_database_name()
    collection_name = get_collection_name()

    try:
        db = client[db_name]
        collection = db[collection_name]

        query_filter = {f"data.{field}": value}

        if partition_key:
            query_filter["partition_key"] = partition_key

        cursor = collection.find(query_filter).limit(limit)

        items = []
        total_count = 0
        for doc in cursor:
            doc_data = doc.get("data", {})
            doc_data["_id"] = str(doc["_id"])
            if "partition_key" in doc:
                doc_data["partition_key"] = doc["partition_key"]
            items.append(QueryResultItem(document_id=str(doc["_id"]), data=doc_data))
            total_count += 1

        return QueryResponse(
            field=field,
            value=value,
            partition_key=partition_key,
            items=items,
            total_count=total_count,
        )
    except PyMongoError as e:
        return QueryResponse(
            field=field,
            value=value,
            partition_key=partition_key,
            items=[],
            total_count=0,
            error=str(e),
        )
    finally:
        client.close()


if __name__ == "__main__":
    response = query_documents("status", "active")
    print(response)
