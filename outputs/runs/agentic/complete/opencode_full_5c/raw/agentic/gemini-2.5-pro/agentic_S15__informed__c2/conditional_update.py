from botocore.exceptions import ClientError
from database_client import get_table
from database_models import UpsertResponse


def conditional_update(
    document_id: str, new_content: str, expected_version: int
) -> UpsertResponse:
    """
    Updates a document only if the provided version matches the one in the database.

    Args:
        document_id: The ID of the document to update.
        new_content: The new content for the document.
        expected_version: The version of the document the caller expects to be updating.

    Returns:
        An UpsertResponse indicating success or failure.
    """
    table = get_table()
    new_version = expected_version + 1
    try:
        table.update_item(
            Key={"document_id": document_id},
            UpdateExpression="SET content = :c, #v = :nv",
            ConditionExpression="#v = :ev",
            ExpressionAttributeNames={"#v": "version"},
            ExpressionAttributeValues={
                ":c": new_content,
                ":nv": new_version,
                ":ev": expected_version,
            },
        )
        return {"success": True, "document_id": document_id, "version": new_version}
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print("Conditional check failed: Document version is outdated.")
        else:
            print(f"An error occurred: {e}")
        return {
            "success": False,
            "document_id": document_id,
            "version": expected_version,
        }
