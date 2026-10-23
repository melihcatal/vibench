import boto3
import os
from database_client import get_dynamodb_client

def query_documents(table_name: str, key_condition_expression: str, expression_attribute_values: dict, expression_attribute_names: dict = None):
    """
    Queries documents by a field value or partition-style key from DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    try:
        query_params = {
            'TableName': table_name,
            'KeyConditionExpression': key_condition_expression,
            'ExpressionAttributeValues': expression_attribute_values
        }
        if expression_attribute_names:
            query_params['ExpressionAttributeNames'] = expression_attribute_names

        response = dynamodb.query(**query_params)
        items = response.get('Items', [])
        print(f"Queried documents: {items}")
        return items
    except Exception as e:
        print(f"Error querying documents: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires AWS credentials and a DynamoDB table)
    # os.environ['AWS_REGION'] = 'us-east-1' # Example
    # os.environ['DYNAMODB_TABLE_NAME'] = 'MyDocumentsTable' # Example
    # table_name = os.getenv('DYNAMODB_TABLE_NAME')

    # if table_name:
    #     # Example: Query documents where 'category' is 'books'
    #     # Assuming 'category' is a partition key or part of a composite key
    #     key_condition_expression = '#cat = :category_val'
    #     expression_attribute_values = {
    #         ':category_val': {'S': 'books'}
    #     }
    #     expression_attribute_names = {
    #         '#cat': 'category'
    #     }
    #     query_documents(table_name, key_condition_expression, expression_attribute_values, expression_attribute_names)
    # else:
    #     print("DYNAMODB_TABLE_NAME environment variable not set.")
