import os
import boto3
from botocore.exceptions import ClientError

def store_onboarding_note(user_id: str, note_id: str, content: str, metadata: dict):
    """
    Persists an onboarding note in Amazon DynamoDB.
    """
    table_name = os.environ.get("DYNAMODB_NOTES_TABLE")
    if not table_name:
        raise ValueError("DYNAMODB_NOTES_TABLE environment variable is not set.")

    # Using default credentials from environment (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    item = {
        'userId': user_id,
        'noteId': note_id,
        'content': content,
        'metadata': metadata
    }

    try:
        table.put_item(Item=item)
        return {"status": "success", "userId": user_id, "noteId": note_id}
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        raise RuntimeError(f"DynamoDB put_item failed ({error_code}): {error_message}") from e
