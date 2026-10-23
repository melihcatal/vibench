import boto3
from database_client import client

TABLE_NAME = 'Documents'


def upsert_document(document):
    '''Insert or replace a document in DynamoDB by its primary key.'''
    try:
        client.put_item(TableName=TABLE_NAME, Item=document)
    except Exception as e:
        raise RuntimeError(f'DynamoDB upsert failed: {e}')

def fetch_document(key):
    '''Retrieve a document by its primary key.'''
    try:
        response = client.get_item(TableName=TABLE_NAME, Key={'id': {'S': key}})
        return response.get('Item')
    except Exception as e:
        raise RuntimeError(f'DynamoDB fetch failed: {e}')

def query_documents(partition_value):
    '''Query documents by partition key (id). Adjust expression for other keys as needed.'''
    try:
        response = client.query(
            TableName=TABLE_NAME,
            KeyConditionExpression=boto3.dynamodb.conditions.Key('id').eq(partition_value)
        )
        return response.get('Items', [])
    except Exception as e:
        raise RuntimeError(f'DynamoDB query failed: {e}')

def conditional_update(key, update_expr, condition_expr=None):
    '''Perform a version‑aware or conditional update on a single document.'''
    try:
        client.update_item(
            TableName=TABLE_NAME,
            Key={'id': {'S': key}},
            UpdateExpression=update_expr,
            ConditionExpression=condition_expr
        )
    except Exception as e:
        raise RuntimeError(f'DynamoDB conditional update failed: {e}')
