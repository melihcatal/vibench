from typing import Dict, Any, List
from database_client import DatabaseClient
from database_models import QueryRequest, QueryResponse, normalize_document


def query_documents(
    field_name: str, field_value: Any, partition_key: str = None
) -> List[Dict[str, Any]]:
    """Query documents in Azure Cosmos DB NoSQL store by field value."""
    client = DatabaseClient().get_container()
    request = QueryRequest(
        field_name=field_name, field_value=field_value, partition_key=partition_key
    )

    query = f"SELECT * FROM c WHERE c.{request.field_name} = @value"
    parameters = [{"name": "@value", "value": request.field_value}]

    if request.partition_key:
        query += " AND c.partition_key = @partition_key"
        parameters.append({"name": "@partition_key", "value": request.partition_key})

    results = list(
        client.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=not request.partition_key,
        )
    )

    return QueryResponse(documents=[normalize_document(doc) for doc in results]).dict()[
        "documents"
    ]
