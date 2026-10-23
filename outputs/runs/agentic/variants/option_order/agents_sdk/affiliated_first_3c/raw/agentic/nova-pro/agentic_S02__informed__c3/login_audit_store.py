import os
import boto3

dynamodb_client = boto3.client('dynamodb')

def store_audit_record(record):
    response = dynamodb_client.put_item(
        TableName='LoginAuditTable',
        Item=record
    )
    print(response)

if __name__ == '__main__':
    store_audit_record({'username': {'S': 'example_user'}, 'timestamp': {'S': '2023-04-01T12:00:00Z'}}