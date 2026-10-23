from database_client import get_db_table
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def conditional_update_document(
    document_id: str, new_content: str, expected_version: int
) -> bool:
    """
    Updates a document's content only if the provided version matches the
    one in the database. It also increments the version number.

    Args:
        document_id: The ID of the document to update.
        new_content: The new content for the document.
        expected_version: The version number that the item is expected to have.

    Returns:
        True if the update was successful, False otherwise.
    """
    try:
        table = get_db_table()
        table.update_item(
            Key={"id": document_id},
            UpdateExpression="SET content = :c, version = version + :inc",
            ConditionExpression="version = :v",
            ExpressionAttributeValues={
                ":c": new_content,
                ":v": expected_version,
                ":inc": 1,
            },
            ReturnValues="UPDATED_NEW",
        )
        logger.info(f"Successfully updated document {document_id} to version {expected_version + 1}")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            logger.warning(
                "Conditional update for document %s failed. "
                "The provided version %s is outdated.",
                document_id,
                expected_version,
            )
        else:
            logger.error(
                "Couldn't update document %s. Here's why: %s: %s",
                document_id,
                e.response["Error"]["Code"],
                e.response["Error"]["Message"],
            )
        return False
