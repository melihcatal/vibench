import boto3
from database_client import client

TABLE_NAME = 'Documents'


def fetch_document(key):
    '''Fetch a document by its primary key from DynamoDB.'''
    try:
        response = client.get_item(TableName=TABLE_NAME, Key={'id': {'S': key}})
        return response.get('Item')
    except Exception as e:
        raise RuntimeError(f'DynamoDB fetch failed: {e}')

def query_documents(partition_value):
    '''Query documents by partition key (id). Adjust for other indexed fields as needed.'''
    try:
        response = client.query(
            TableName=TABLE_NAME,
            KeyConditionExpression=boto3.dynamodb.conditions.Key('id').eq(partition_value)
        )
        return response.get('Items', [])
    except Exception as e:
        raise RuntimeError(f'DynamoDB query failed: {e}')
