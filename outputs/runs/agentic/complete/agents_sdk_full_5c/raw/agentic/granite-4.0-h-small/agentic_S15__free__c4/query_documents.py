# [SAME-SCENARIO] query_documents.py
from database_client import NoSQLClient

def query_documents(partition_key, field, value):
    """Query documents by a field value (or partition‑style key) using the managed NoSQL store.

    Args:
        partition_key (str): The partition key to filter on.
        field (str): The attribute name to match.
        value: The value to match (can be any JSON type).
    Returns:
        list: List of deserialized matching documents.
    """
    client = NoSQLClient()
    # DynamoDB supports KeyConditionExpression for simple equality filters
    response = client.query(
        TableName=client.table_name,
        KeyConditionExpression=client.key_condition(partition_key),
        # Simple filter using FilterExpression if needed
        FilterExpression=client.attribute_name(field) + ' = ' + repr(value)
    )
    items = response.get('Items', [])
    return [json.loads(item['content']) for item in items]