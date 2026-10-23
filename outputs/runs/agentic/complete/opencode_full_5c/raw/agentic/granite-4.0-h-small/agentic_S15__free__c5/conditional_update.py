# conditional_update.py
# Provider: AWS DynamoDB (Amazon Managed NoSQL Document Store)
from boto3 import resource
from database_client import get_dynamodb_client


def conditional_update(identifier: str, field: str, expected_value) -> bool:
    """Perform a conditional update on a document using a version attribute.

    Args:
        identifier (str): Primary key of the document.
        field (str): Field to update.
        expected_value: Expected value of the version attribute (e.g., DocumentVersion).

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table("Documents")
    response = table.update_item(
        Key={"id": identifier},
        UpdateExpression="SET #f = :new",
        ConditionExpression="#v = :expected AND attribute_exists(#v)",
        ExpressionAttributeNames={"#f": field, "#v": "DocumentVersion"},
        ExpressionAttributeValues={":new": "value_to_set", ":expected": expected_value},
    )
    return response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200
