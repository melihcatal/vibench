from database_client import get_db_table
from botocore.exceptions import ClientError


def conditional_update(document_id: str, new_content: dict, expected_version: int):
    table = get_db_table()

    try:
        response = table.update_item(
            Key={"documentId": document_id},
            UpdateExpression="set content = :c, version = :v_new",
            ConditionExpression="version = :v_old",
            ExpressionAttributeValues={
                ":c": new_content,
                ":v_new": expected_version + 1,
                ":v_old": expected_version,
            },
            ReturnValues="UPDATED_NEW",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print(f"Update failed for document {document_id} due to version mismatch.")
            return None
        else:
            raise
    return response
