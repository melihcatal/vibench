from botocore.exceptions import ClientError
from database_client import get_dynamodb_table
from database_models import ConditionalUpdateRequest

def conditional_update(request: ConditionalUpdateRequest):
    """
    Updates a document in Amazon DynamoDB only if the version matches.
    Implements optimistic locking.

    Args:
        request: A dictionary containing the document ID, expected version,
                 and the new content to update.

    Returns:
        The updated item attributes upon success, or None on failure.
    """
    table = get_dynamodb_table()
    document_id = request['id']
    expected_version = request['expected_version']
    new_content = request['new_content']
    
    new_version = expected_version + 1

    try:
        response = table.update_item(
            Key={'id': document_id},
            UpdateExpression="SET content = :c, #v = :nv",
            ConditionExpression="#v = :ev",
            ExpressionAttributeNames={
                '#v': 'version'
            },
            ExpressionAttributeValues={
                ':c': new_content,
                ':ev': expected_version,
                ':nv': new_version
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Document {document_id} updated to version {new_version}")
        return response['Attributes']
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(f"Update failed for document {document_id}: Version mismatch (expected {expected_version}).")
        else:
            print(f"An error occurred: {e.response['Error']['Message']}")
        return None
