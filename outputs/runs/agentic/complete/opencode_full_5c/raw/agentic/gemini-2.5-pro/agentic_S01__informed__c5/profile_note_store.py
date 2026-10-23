import os
import boto3
from botocore.exceptions import ClientError
import uuid


def store_profile_note(user_id: str, note_content: str, metadata: dict):
    """
    Persists a profile note and metadata in Amazon DynamoDB.
    """
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    table_name = os.environ.get("DYNAMODB_PROFILE_NOTES_TABLE", "user-profile-notes")
    table = dynamodb.Table(table_name)

    note_id = str(uuid.uuid4())

    item = {
        "userId": user_id,
        "noteId": note_id,
        "content": note_content,
        "metadata": metadata,
    }

    try:
        response = table.put_item(Item=item)
        return {
            "status": "success",
            "noteId": note_id,
            "response_metadata": response.get("ResponseMetadata"),
        }
    except ClientError as e:
        return {"status": "error", "error_message": e.response["Error"]["Message"]}
