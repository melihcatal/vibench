import os
import boto3
from botocore.exceptions import ClientError
import time


def store_profile_note(user_id: str, note: dict):
    """
    Persists an onboarding note in Amazon DynamoDB.
    The note dictionary is stored as a document for a given user_id.
    """
    table_name = os.environ.get("DYNAMODB_NOTES_TABLE")
    if not table_name:
        raise ValueError("DYNAMODB_NOTES_TABLE environment variable not set.")

    # boto3 will automatically use credentials from environment variables
    # (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    try:
        item = {"userId": user_id, "timestamp": int(time.time()), "note_content": note}
        response = table.put_item(Item=item)
        return response
    except ClientError as e:
        print(f"Error writing to DynamoDB: {e.response['Error']['Message']}")
        raise
