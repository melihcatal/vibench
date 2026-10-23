from typing import Dict, List, Optional, Any
from database_client import DatabaseClient
from database_models import QueryRequest, QueryResponse, normalize_document


def query_documents(
    field_name: str, field_value: Any, partition_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    client = DatabaseClient().get_container()
    query_request = QueryRequest(
        field_name=field_name, field_value=field_value, partition_key=partition_key
    )

    query = f"SELECT * FROM c WHERE c.{query_request.field_name} = @value"
    parameters = [{"name": "@value", "value": query_request.field_value}]

    if query_request.partition_key:
        query += " AND c.partitionKey = @partitionKey"
        parameters.append(
            {"name": "@partitionKey", "value": query_request.partition_key}
        )

    results = list(
        client.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=not query_request.partition_key,
        )
    )

    return QueryResponse(documents=[normalize_document(doc) for doc in results]).dict(
        by_alias=True
    )
