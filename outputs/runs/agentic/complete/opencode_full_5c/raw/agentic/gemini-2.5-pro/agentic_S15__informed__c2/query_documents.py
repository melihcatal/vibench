from boto3.dynamodb.conditions import Key
from database_client import get_table
from database_models import QueryResponse


def query_documents(author: str) -> QueryResponse:
    """
    Queries documents by the author's name (assuming it's a partition key or part of an index).
    For this example, we assume 'author' is a global secondary index partition key 'author-index'.

    Args:
        author: The author to query for.

    Returns:
        A QueryResponse containing the list of documents.
    """
    table = get_table()
    try:
        response = table.query(
            IndexName="author-index", KeyConditionExpression=Key("author").eq(author)
        )
        return {"success": True, "documents": response.get("Items", [])}
    except Exception as e:
        # Fallback for tables without the index, querying the main table if schema allows
        # This is inefficient and should be avoided in production without an index
        try:
            response = table.scan(FilterExpression=Key("author").eq(author))
            return {"success": True, "documents": response.get("Items", [])}
        except Exception as scan_e:
            print(f"Error querying documents: {scan_e}")
            return {"success": False, "documents": []}
