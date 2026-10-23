import os
from database_client import NoSQLClient
from database_models import Document

def conditional_update(primary_id: str, update_fields: dict, expected_version: int | None = None) -> bool:
    """Conditionally update a document using version attribute for concurrency control.

    Uses Amazon DynamoDB's UpdateItem with ConditionExpression based on a
    'version' attribute. If expected_version is supplied, the update will only
    succeed when the stored version matches.
    """
    client = NoSQLClient()
    expression = 'SET ' + ', '.join(f"{k} = :{k}" for k in update_fields)
    condition = 'attribute_exists(version)'  # ensures document exists
    if expected_version is not None:
        condition += f' AND version = :expected'

    response = client.update_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Key={'id': {'S': primary_id}},
        UpdateExpression=expression,
        ExpressionAttributeValues={
            **{f":{k}": {'S': str(v)} for k, v in update_fields.items()},
            ":expected": {'N': str(expected_version)} if expected_version is not None else {}
        },
        ConditionExpression=condition
    )
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200
