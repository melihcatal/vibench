from database_client import get_db_table
from botocore.exceptions import ClientError
from typing import Optional, Dict

def update_document_content_if_version_matches(
    table_name: str,
    document_id: str,
    new_content: str,
    expected_version: int
) -> Optional[Dict]:
    """
    Conditionally updates a document's content in Amazon DynamoDB.

    The update succeeds only if the document's 'version' attribute
    matches the expected_version. If successful, the version is incremented.

    :param table_name: The name of the DynamoDB table.
    :param document_id: The ID of the document to update.
    :param new_content: The new content to set.
    :param expected_version: The version number the document must have for the update to occur.
    :return: The updated document attributes, or None if the condition check failed.
    """
    table = get_db_table(table_name)
    if not table:
        raise ConnectionError("Could not connect to the database.")

    try:
        response = table.update_item(
            Key={'id': document_id},
            UpdateExpression="SET content = :c, version = version + :inc",
            ConditionExpression="version = :v",
            ExpressionAttributeValues={
                ':c': new_content,
                ':v': expected_version,
                ':inc': 1
            },
            ReturnValues="ALL_NEW"
        )
        return response.get('Attributes')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print(f"Conditional check failed for document {document_id} with version {expected_version}.")
            return None
        else:
            print(f"Error updating document {document_id}: {e.response['Error']['Message']}")
            raise
