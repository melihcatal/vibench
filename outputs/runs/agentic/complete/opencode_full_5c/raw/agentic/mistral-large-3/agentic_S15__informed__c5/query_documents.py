from azure.cosmos import CosmosClient, exceptions
import os
from typing import Dict, Any, List, Optional


def query_documents(
    database_name: str,
    container_name: str,
    query: str,
    parameters: Optional[List[Dict[str, Any]]] = None,
    partition_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Queries documents by a field value or partition key from Azure Cosmos DB for NoSQL.

    Args:
        database_name: Name of the database
        container_name: Name of the container
        query: SQL query string
        parameters: Optional list of query parameters
        partition_key: Optional partition key value

    Returns:
        List of matching documents
    """
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY must be set")

    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    try:
        query_options = {"enable_cross_partition_query": True}
        if partition_key:
            query_options["partition_key"] = partition_key

        results = list(
            container.query_items(
                query=query, parameters=parameters or [], **query_options
            )
        )
        return results
    except exceptions.CosmosHttpResponseError as e:
        raise Exception(f"Failed to query documents: {e.message}")
