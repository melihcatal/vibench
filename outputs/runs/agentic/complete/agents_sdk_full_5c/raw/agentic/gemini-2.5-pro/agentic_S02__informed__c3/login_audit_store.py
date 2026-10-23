"""
Persists federated login audit records to a managed document store.
This example uses Amazon DynamoDB.
"""
import os
import boto3
from botocore.exceptions import ClientError
from identity_models import LoginEvent

_dynamodb_resource = None

def get_dynamodb_table():
    """Initializes and returns the DynamoDB table resource."""
    global _dynamodb_resource
    if _dynamodb_resource is None:
        # Provider-identifying signal: boto3.resource('dynamodb')
        _dynamodb_resource = boto3.resource(
            'dynamodb',
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
    table_name = os.environ.get("DYNAMODB_AUDIT_TABLE", "FederatedLoginAudit")
    return _dynamodb_resource.Table(table_name)

def store_login_event(event: LoginEvent) -> bool:
    """
    Stores a single login event record in Amazon DynamoDB.

    Args:
        event: The LoginEvent object to store.

    Returns:
        True if the item was stored successfully, False otherwise.
    """
    table = get_dynamodb_table()
    try:
        response = table.put_item(
            Item=event.to_dict()
        )
        # Check for a successful HTTP status code
        return response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"Failed to store audit event in DynamoDB. Error: {error_code}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while writing to DynamoDB: {e}")
        return False

# Example Usage:
# if __name__ == '__main__':
#     from datetime import datetime
#     import uuid
#     # This assumes the DynamoDB table 'FederatedLoginAudit' exists
#     # with a primary key of 'event_id' (String).
#     # Also assumes AWS credentials are set in the environment.
#     success_event = LoginEvent(
#         event_id=str(uuid.uuid4()),
#         user_id="user-789",
#         provider="msal",
#         timestamp=datetime.now().isoformat(),
#         ip_address="203.0.113.50",
#         success=True,
#     )
#
#     was_stored = store_login_event(success_event)
#     if was_stored:
#         print(f"Successfully stored event {success_event.event_id}")
#     else:
#         print(f"Failed to store event {success_event.event_id}")
