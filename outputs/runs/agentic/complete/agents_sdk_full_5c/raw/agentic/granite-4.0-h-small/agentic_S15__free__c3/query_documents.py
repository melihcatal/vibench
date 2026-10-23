# query_documents.py
# [SAME-SCENARIO] Query documents stored in Azure Cosmos DB (NoSQL)

import os
from database_client import get_cosmos_db_client
from database_models import QueryCriteria, QueryResult

def query_documents(criteria: QueryCriteria) -> QueryResult:
    """Query documents matching the given criteria.

    Criteria should specify a field name and value (e.g., {"status": "active"}).
    """
    client = get_cosmos_db_client()
    container = client.get_container("mydb", "documents")
    # Use SQL query via Cosmos SDK
    query = f"SELECT * FROM c WHERE c.{criteria.field} = @value"
    results = list(container.query_items(
        query=query,
        parameters=[{"name": "@value", "value": criteria.value}]
    ))
    return QueryResult(results=results)
