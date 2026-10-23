import boto3
import os
from database_client import get_dynamodb_client

def conditional_update(table_name: str, key: dict, update_expression: str, expression_attribute_values: dict, condition_expression: str = None, expression_attribute_names: dict = None):
    """
    Applies a conditional or version-aware update to one stored document in DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    try:
        update_params = {
            'TableName': table_name,
            'Key': key,
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_attribute_values,
            'ReturnValues': 'UPDATED_NEW'
        }

        if condition_expression:
            update_params['ConditionExpression'] = condition_expression
        if expression_attribute_names:
            update_params['ExpressionAttributeNames'] = expression_attribute_names

        response = dynamodb.update_item(**update_params)
        print(f"Document updated successfully: {response.get('Attributes')}")
        return response
    except dynamodb.exceptions.ConditionalCheckFailedException:
        print("Conditional check failed: document not updated.")
        raise
    except Exception as e:
        print(f"Error updating document: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires AWS credentials and a DynamoDB table)
    # os.environ['AWS_REGION'] = 'us-east-1' # Example
    # os.environ['DYNAMODB_TABLE_NAME'] = 'MyDocumentsTable' # Example
    # table_name = os.getenv('DYNAMODB_TABLE_NAME')

    # if table_name:
    #     # Example: Update title if current version is 1
    #     key = {'id': {'S': 'doc123'}}
    #     update_expression = 'SET #t = :new_title, version = :new_version'
    #     condition_expression = 'version = :current_version'
    #     expression_attribute_values = {
    #         ':new_title': {'S': 'Updated Document Title'},
    #         ':new_version': {'N': '2'},
    #         ':current_version': {'N': '1'}
    #     }
    #     expression_attribute_names = {
    #         '#t': 'title'
    #     }
    #     conditional_update(table_name, key, update_expression, expression_attribute_values, condition_expression, expression_attribute_names)
    # else:
    #     print("DYNAMODB_TABLE_NAME environment variable not set.")
