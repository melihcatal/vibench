# query_documents.py
# Provider: AWS DynamoDB (Amazon Managed NoSQL Document Store)
from boto3 import resource
from database_client import get_dynamodb_client


def query_documents(partition_key: str, field: str, value) -> list:
    """Query DynamoDB documents that match a field value using a partition key filter.

    Args:
        partition_key (str): The partition (primary) key value to restrict results.
        field (str): Document field name to filter on.
        value: Value to match for the specified field.

    Returns:
        list: List of matching documents (as dicts).
    """
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table("Documents")
    # Simple scan with filter expression; replace with Query if using a secondary index
    response = table.scan(
        FilterExpression=(
            ("#pk = :pk") & (("#attr" == value) if value is not None else True)
        ),
        ExpressionAttributeNames={"#pk": partition_key, "#attr": field},
        ExpressionAttributeValues={":pk": value},
    )
    return response.get("Items", [])
