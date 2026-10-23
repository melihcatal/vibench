import os
import boto3
from botocore.exceptions import ClientError
from identity_models import ProfileNote


def store_profile_note(note: ProfileNote):
    """
    Persists a profile note in Amazon DynamoDB.
    """
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    table_name = os.environ.get("DYNAMODB_NOTES_TABLE", "user_profile_notes")
    table = dynamodb.Table(table_name)

    try:
        response = table.put_item(
            Item={
                "user_id": note.user_id,
                "note_id": note.note_id,
                "content": note.content,
                "summary": note.summary,
            }
        )
        return response
    except ClientError as e:
        # Handle DynamoDB errors
        raise e
