from botocore.exceptions import ClientError
from database_client import get_table

def conditional_update(document_id: str, new_content: str, expected_version: int):
    """
    Updates a document's content only if the version matches.

    This implements optimistic locking in Amazon DynamoDB.

    :param document_id: The ID of the document to update.
    :param new_content: The new content to set.
    :param expected_version: The version number we expect the document to have.
    :return: The HTTP status code from the update response, or an error dict.
    """
    table = get_table()
    new_version = expected_version + 1

    try:
        response = table.update_item(
            Key={'document_id': document_id},
            UpdateExpression="SET content = :c, version = :nv",
            ConditionExpression="version = :ev",
            ExpressionAttributeValues={
                ':c': new_content,
                ':nv': new_version,
                ':ev': expected_version
            },
            ReturnValues="UPDATED_NEW"
        )
        return response['ResponseMetadata']['HTTPStatusCode']
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return {"error": "ConditionalCheckFailedException", "message": "Version mismatch"}
        else:
            raise
