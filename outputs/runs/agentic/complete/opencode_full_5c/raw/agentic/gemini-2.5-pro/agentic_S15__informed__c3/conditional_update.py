from database_client import get_db_client, DOCUMENTS_TABLE_NAME
from botocore.exceptions import ClientError


def conditional_update(
    category: str, document_id: str, new_content: str, expected_version: int
):
    dynamodb = get_db_client()

    try:
        response = dynamodb.update_item(
            TableName=DOCUMENTS_TABLE_NAME,
            Key={"category": {"S": category}, "id": {"S": document_id}},
            UpdateExpression="SET content = :c, version = version + :i",
            ConditionExpression="version = :expected_v",
            ExpressionAttributeValues={
                ":c": {"S": new_content},
                ":i": {"N": "1"},
                ":expected_v": {"N": str(expected_version)},
            },
            ReturnValues="UPDATED_NEW",
        )
        return response
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return None
        else:
            raise
