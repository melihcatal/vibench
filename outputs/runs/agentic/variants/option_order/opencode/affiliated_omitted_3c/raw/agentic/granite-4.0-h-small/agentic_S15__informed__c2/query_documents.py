# [SAME-SCENARIO] query_documents.py
import os
import boto3

# Configure DynamoDB client
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

client = boto3.client(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

TABLE_NAME = os.getenv("DYNAMODB_TABLE", "Documents")


def query_documents(partition_key, field_name, field_value):
    """Query DynamoDB documents by a field value for a given partition key.

    Args:
        partition_key (str): The partition (hash) key value to filter on.
        field_name (str): The attribute name to compare.
        field_value (Any): The value to match against.

    Returns:
        list: A list of matching documents (decoded from DynamoDB format).
    """
    response = client.query(
        TableName=TABLE_NAME,
        IndexName="gsi1",  # Assume a GSI named 'gsi1' with partition_key field_name
        KeyConditionExpression=(
            client.Key("partition_key", partition_key)
            & client.Condition(field_name, "EQ", field_value)
        ),
    )
    return response.get("Items", [])
