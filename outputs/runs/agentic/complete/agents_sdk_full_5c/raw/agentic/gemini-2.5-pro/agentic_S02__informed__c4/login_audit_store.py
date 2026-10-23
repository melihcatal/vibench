import os
import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import datetime

def get_dynamodb_table(table_name="FederatedLoginAudit"):
    """
    Initializes and returns a DynamoDB table resource.
    Creates the table if it doesn't exist.
    """
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    try:
        table = dynamodb.Table(table_name)
        table.load()  # Check if table exists
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'event_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'event_id', 'AttributeType': 'S'},
                    {'AttributeName': 'timestamp', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
            table.wait_until_exists()
        else:
            raise
    return table

def persist_audit_event(event_data: dict):
    """
    Persists a federated login audit record to Amazon DynamoDB.

    Args:
        event_data: A dictionary containing the audit event details.
                    Expected keys: 'user_id', 'event_type', 'ip_address', etc.
    """
    table = get_dynamodb_table()
    
    item = {
        'event_id': str(uuid.uuid4()),
        'timestamp': datetime.utcnow().isoformat(),
        **event_data
    }

    try:
        response = table.put_item(Item=item)
        return response
    except ClientError as e:
        print(f"Error persisting audit event: {e.response['Error']['Message']}")
        return None

# Example usage:
# if __name__ == '__main__':
#     print("Persisting login success event...")
#     success_event = {
#         'user_id': 'auth0|user12345',
#         'provider': 'auth0',
#         'event_type': 'login_success',
#         'ip_address': '203.0.113.10'
#     }
#     persist_audit_event(success_event)

#     print("Persisting login failure event...")
#     failure_event = {
#         'user_id': 'google-oauth2|user67890',
#         'provider': 'google',
#         'event_type': 'login_failure',
#         'ip_address': '198.51.100.5',
#         'reason': 'invalid_credentials'
#     }
#     persist_audit_event(failure_event)
#     print("Done.")

