from boto3.dynamodb.conditions import Key
from database_client import get_dynamodb_table

def query_documents_by_partition_key(partition_key: str):
    """
    Queries documents from DynamoDB using a partition key.
    This assumes a Global Secondary Index (GSI) named 'PartitionKeyIndex'
    exists on the table with 'partitionKey' as its hash key.

    Args:
        partition_key: The partition key value to query for.
    
    Returns:
        A list of document items that match the query.
    """
    table = get_dynamodb_table()
    response = table.query(
        IndexName='PartitionKeyIndex',
        KeyConditionExpression=Key('partitionKey').eq(partition_key)
    )
    return response.get('Items', [])
