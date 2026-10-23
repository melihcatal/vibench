from database_client import CosmosDBClient
from database_models import Document, QueryResult
from typing import Any, Dict, Optional, List

def query_documents(query_string: str, parameters: Optional[List[Dict[str, Any]]] = None, max_item_count: int = -1) -> QueryResult:
    cosmos_client = CosmosDBClient()
    # Example query_string: "SELECT * FROM c WHERE c.category = @category"
    # Example parameters: [{"name": "@category", "value": "books"}]
    
    # Default to a simple query if none provided for example purposes
    if not query_string:
        query_string = "SELECT * FROM c"

    query_results = cosmos_client.container.query_items(
        query=query_string,
        parameters=parameters if parameters is not None else [],
        enable_cross_partition_query=True, # Enable if queries might span multiple partitions
        max_item_count=max_item_count
    )

    documents = [Document.from_dict(item) for item in query_results]
    # Cosmos DB SDK handles continuation tokens internally for iterators, but if we need it explicitly for stateless pagination,
    # we would need to implement it with feed_options and a custom loop. For simplicity, we return all results or max_item_count.
    return QueryResult(documents=documents)
