import os
import boto3
from botocore.exceptions import ClientError

# Managed NoSQL Document Store: Amazon DynamoDB
TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'onboarding-notes')
REGION = os.getenv('AWS_REGION', 'us-east-1')

def store_note(user_id: str, note_id: str, content: str) -> dict:
    """Persist an onboarding note (or any support metadata) in DynamoDB.

    Each note is stored under a composite key (user_id, note_id).
    Returns the response from DynamoDB PutItem API.
    """
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(TABLE_NAME)
    try:
        response = table.put_item(
            Item={
                'user_id': user_id,
                'note_id': note_id,
                'content': content,
                'created_at': str(boto3.utils.now())  # placeholder for timestamp
            }
        )
        return response
    except ClientError as e:
        raise RuntimeError(f"Failed to store note: {e}")