import boto3
from database_client import client

TABLE_NAME = 'Documents'


def conditional_update(key, update_expression, condition_expression=None):
    '''Apply a conditional update to a document identified by its primary key.

    update_expression: DynamoDB UpdateExpression string (e.g., 'SET #n = :val').
    condition_expression: Optional DynamoDB ConditionExpression (e.g., '#v = :ver').
    '''
    try:
        client.update_item(
            TableName=TABLE_NAME,
            Key={'id': {'S': key}},
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression
        )
    except Exception as e:
        raise RuntimeError(f'DynamoDB conditional update failed: {e}')

# Example usage:
# conditional_update(
#     key='doc-123',
#     update_expression='SET #t = :title, #c = :content',
#     condition_expression='#v = :expected',
# )
