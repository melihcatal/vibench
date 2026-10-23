from database_client import get_db_table
from boto3.dynamodb.conditions import Key
from typing import List, Dict, Any


def query_documents_by_author(author: str) -> List[Dict[str, Any]]:
    table = get_db_table()
    # This query requires a Global Secondary Index (GSI) on the 'author' attribute.
    # The GSI should be named 'author-index'.
    response = table.query(
        IndexName="author-index", KeyConditionExpression=Key("author").eq(author)
    )
    return response.get("Items", [])
