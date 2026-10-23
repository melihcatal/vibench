import boto3
import os
from database_client import get_dynamodb_client

def conditional_update(table_name: str, document_id: str, updates: dict, expected_version: int) -> dict:
    """
    Applies a conditional or version-aware update to one stored document in DynamoDB.
    This function will update the document only if its 'version' attribute matches the expected_version.
    It also increments the version number upon successful update.
    """
    dynamodb = get_dynamodb_client()
    update_expression_parts = []
    expression_attribute_values = {':expectedVersion': {'N': str(expected_version)}}
    expression_attribute_names = {}
    
    for k, v in updates.items():
        # DynamoDB requires type specification for values
        # Assuming simple string and number types for demonstration
        if isinstance(v, str):
            expression_attribute_values[f':{k}'] = {'S': v}
        elif isinstance(v, (int, float)):
            expression_attribute_values[f':{k}'] = {'N': str(v)}
        # Add other types as needed
        expression_attribute_names[f'#{k}'] = k
        update_expression_parts.append(f'#{k} = :{k}')

    # Always update the version number
    update_expression_parts.append('#version = :newVersion')
    expression_attribute_values[':newVersion'] = {'N': str(expected_version + 1)}
    expression_attribute_names['#version'] = 'version'

    update_expression = 'SET ' + ', '.join(update_expression_parts)
    condition_expression = '#version = :expectedVersion'

    try:
        response = dynamodb.update_item(
            TableName=table_name,
            Key={
                'id': {'S': document_id}
            },
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="ALL_NEW"
        )
        print(f"Document updated successfully. New attributes: {response.get('Attributes')}")
        from database_models import deserialize_dynamodb_item
        return deserialize_dynamodb_item(response.get('Attributes'))
    except dynamodb.exceptions.ConditionalCheckFailedException:
        print(f"Conditional update failed for document {document_id}. Version mismatch. Expected {expected_version}.")
        return None
    except Exception as e:
        print(f"Error performing conditional update: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION env vars)
    # table_name = os.getenv("DYNAMODB_TABLE_NAME", "my-documents-table")
    # document_id = "doc123"
    # updates = {
    #     "content": "This is the updated content of my first document."
    # }
    # # Assuming the current version of doc123 is 1
    # updated_doc = conditional_update(table_name, document_id, updates, 1)
    # if updated_doc:
    #     print(f"Updated document: {updated_doc}")
    
    # # Attempting to update with an old version should fail
    # print("\nAttempting update with wrong version...")
    # failed_update = conditional_update(table_name, document_id, {"content": "This update should fail"}, 1)
    # if not failed_update:
    #     print("Update with wrong version correctly failed.")
    pass
