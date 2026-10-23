from botocore.exceptions import ClientError
from database_client import get_db_table

def update_document_content_if_version_matches(document_id: str, new_content: str, expected_version: int):
    """
    Conditionally updates a document's content in AWS DynamoDB.

    The update succeeds only if the `version` attribute in the database
    matches the `expected_version`. If successful, the version is incremented.
    This pattern is used for optimistic locking.

    Provider: AWS DynamoDB
    """
    table = get_db_table()
    try:
        response = table.update_item(
            Key={'document_id': document_id},
            UpdateExpression="set content = :c, version = :v_new",
            ConditionExpression="version = :v_old",
            ExpressionAttributeValues={
                ':c': new_content,
                ':v_new': expected_version + 1,
                ':v_old': expected_version
            },
            ReturnValues="UPDATED_NEW"
        )
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(f"Condition check failed for document {document_id}: Version mismatch.")
            return None
        else:
            # Re-raise the exception if it's not the one we're handling.
            raise
