import os
from botocore.exceptions import ClientError
from database_models import TABLE_NAME
from database_client import get_table

def conditional_update_document(doc_id: str, new_content: str, expected_version: int):
    """
    Conditionally updates a document's content field if the version matches.

    :param doc_id: The ID of the document to update.
    :param new_content: The new content for the 'content' field.
    :param expected_version: The expected 'version' of the document for the update to succeed.
    :return: The response from DynamoDB.
    """
    table = get_table(TABLE_NAME)
    try:
        new_version = expected_version + 1
        response = table.update_item(
            Key={'id': doc_id},
            UpdateExpression="SET content = :c, version = :nv",
            ConditionExpression="version = :ev",
            ExpressionAttributeValues={
                ':c': new_content,
                ':nv': new_version,
                ':ev': expected_version,
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Successfully updated document with id: {doc_id} to version {new_version}")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(f"Conditional update failed for id: {doc_id}. Version mismatch (expected {expected_version}).")
        else:
            print(f"Error updating document: {e.response['Error']['Message']}")
        raise
