from botocore.exceptions import ClientError
from database_client import get_boto_client, get_table_name

def update_content_if_version_matches(document_id: str, new_content: str, expected_version: int):
    """
    Updates a document's content only if its current version matches the expected version.
    This implements optimistic locking.

    :param document_id: The ID of the document to update.
    :param new_content: The new content to set.
    :param expected_version: The version number required for the update to proceed.
    :return: The response from DynamoDB or None if the update fails.
    """
    dynamodb = get_boto_client()
    table_name = get_table_name()
    new_version = expected_version + 1

    try:
        response = dynamodb.update_item(
            TableName=table_name,
            Key={'documentId': {'S': document_id}},
            UpdateExpression='SET content = :c, #v = :nv',
            ConditionExpression='#v = :ev',
            ExpressionAttributeNames={
                '#v': 'version'
            },
            ExpressionAttributeValues={
                ':c': {'S': new_content},
                ':ev': {'N': str(expected_version)},
                ':nv': {'N': str(new_version)}
            },
            ReturnValues='UPDATED_NEW'
        )
        print(f"Successfully updated document {document_id} to version {new_version}")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(f"Update failed for {document_id}: version mismatch (expected {expected_version}).")
        else:
            print(f"Error updating document: {e.response['Error']['Message']}")
        return None

