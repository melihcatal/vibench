import os
from database_client import get_dynamodb_client
from database_models import Document

def query_documents(partition_key: str, value: str):
    """Query DynamoDB for documents where a specific attribute equals a value.

    This uses DynamoDB's Query API assuming the queried attribute is indexed.

    Args:
        partition_key (str): The partition key attribute name (e.g., 'type').
        value (str): The value to match against the partition key.

    Returns:
        list[dict]: A list of deserialized document dictionaries.
    """
    client = get_dynamodb_client()
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise RuntimeError("DYNAMODB_TABLE_NAME environment variable not set")

    response = client.query(
        TableName=table_name,
        KeyConditionExpression={
            "ExpressionAttributeNames": {"#PK": partition_key},
            "ExpressionAttributeValues": {
                ":v": {"S": value}
            },
            "ConditionExpression": "#PK = :v"
        },
    )
    items = response.get("Items", [])
    # Convert each DynamoDB map to a Document and then to a plain dict
    docs = [Document.from_dynamodb_map(item).to_dict() for item in items]
    return docs
