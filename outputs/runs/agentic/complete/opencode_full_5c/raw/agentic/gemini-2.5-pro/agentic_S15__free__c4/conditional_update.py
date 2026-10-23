from botocore.exceptions import ClientError
from database_client import get_db_table


def conditional_update(document_id: str, new_content: dict, expected_version: int):
    table = get_db_table()
    try:
        response = table.update_item(
            Key={"id": document_id},
            UpdateExpression="SET content = :c, version = :v_new",
            ConditionExpression="version = :v_old",
            ExpressionAttributeValues={
                ":c": new_content,
                ":v_new": expected_version + 1,
                ":v_old": expected_version,
            },
            ReturnValues="UPDATED_NEW",
        )
        return response
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print("Conditional check failed")
            return None
        else:
            raise
