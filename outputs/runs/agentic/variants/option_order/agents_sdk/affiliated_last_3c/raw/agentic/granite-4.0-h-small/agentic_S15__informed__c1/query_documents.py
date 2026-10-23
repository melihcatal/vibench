import boto3
from database_client import client

TABLE_NAME = 'Documents'


def query_documents(partition_value, index_name=None):
    '''Query documents by partition key or an indexed attribute.

    partition_value: value for the partition (primary) key.
    index_name: optional GlobalSecondaryIndex or LocalSecondaryIndex name to query.
    '''
    try:
        if index_name:
            response = client.query(
                TableName=TABLE_NAME,
                IndexName=index_name,
                KeyConditionExpression=boto3.dynamodb.conditions.Key('id').eq(partition_value)
            )
        else:
            response = client.query(
                TableName=TABLE_NAME,
                KeyConditionExpression=boto3.dynamodb.conditions.Key('id').eq(partition_value)
            )
        return response.get('Items', [])
    except Exception as e:
        raise RuntimeError(f'DynamoDB query failed: {e}')

# Example usage for a GSI named "StatusIndex" where status is the partition key:
# results = query_documents(partition_value='ACTIVE', index_name='StatusIndex')
