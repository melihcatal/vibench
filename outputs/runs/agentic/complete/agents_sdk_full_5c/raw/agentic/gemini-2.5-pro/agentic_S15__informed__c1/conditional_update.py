from botocore.exceptions import ClientError
from database_client import get_dynamodb_table

def conditional_update_document(
    document_id: str,
    new_content: str,
    expected_version: int
):
    """
    Updates a document only if the provided version matches the one in the database.
    This implements optimistic locking. It also increments the version number.

    Args:
        document_id: The ID of the document to update.
        new_content: The new content for the document.
        expected_version: The version number that the document is expected to have.
    
    Returns:
        The updated attributes of the document if the update succeeds.
    
    Raises:
        ValueError: If the conditional check fails (i.e., versions mismatch).
        Exception: For other Boto3/DynamoDB errors.
    """
    table = get_dynamodb_table()
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
            ReturnValues="UPDATED_NEW"
        )
        return response.get('Attributes')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise ValueError(f"Conditional check failed for document {document_id}. Version mismatch.")
        else:
            # Re-raise other exceptions
            raise e
