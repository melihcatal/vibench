from typing import List, Dict, Any
from boto3.dynamodb.conditions import Key
from database_client import get_table
from database_models import normalize_document_from_db

def query_documents(partition_key: str) -> List[Dict[str, Any]]:
    """
    Queries for documents using the partition key.

    Args:
        partition_key: The partition key to query for.

    Returns:
        A list of documents matching the query.
    """
    table = get_table()
    
    # This queries for all items with a specific partition key.
    # The key name 'partitionKey' must match the table's schema.
    response = table.query(
        KeyConditionExpression=Key('partitionKey').eq(partition_key)
    )
    
    items = response.get('Items', [])
    return [normalize_document_from_db(item) for item in items]
