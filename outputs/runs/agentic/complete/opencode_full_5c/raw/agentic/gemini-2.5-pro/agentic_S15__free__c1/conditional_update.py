from botocore.exceptions import ClientError
from database_client import get_table


def conditional_update(document_id: str, new_content: str, expected_version: int):
    """
    Updates a document's content only if the version matches.
    Increments the version number upon successful update.
    """
    table = get_table()
    try:
        response = table.update_item(
            Key={"document_id": document_id},
            UpdateExpression="set content = :c, version = :v_new",
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
            print("Conditional check failed: Document version is outdated.")
            return None
        else:
            raise
