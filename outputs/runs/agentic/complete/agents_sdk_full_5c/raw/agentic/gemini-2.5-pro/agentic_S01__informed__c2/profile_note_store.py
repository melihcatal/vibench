# profile_note_store.py
import os
import boto3
from botocore.exceptions import ClientError

def save_onboarding_note(user_id: str, note: dict):
    """
    Persists an onboarding note for a user in Amazon DynamoDB.
    """
    table_name = os.environ.get("DYNAMODB_NOTES_TABLE", "onboarding-notes")
    # AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) and region
    # should be configured in the environment.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        item_to_save = {
            'userId': user_id,
            **note
        }
        response = table.put_item(Item=item_to_save)
        print(f"Successfully saved note for user {user_id}.")
        return response
    except ClientError as e:
        print(f"Error saving note to DynamoDB: {e.response['Error']['Message']}")
        raise
