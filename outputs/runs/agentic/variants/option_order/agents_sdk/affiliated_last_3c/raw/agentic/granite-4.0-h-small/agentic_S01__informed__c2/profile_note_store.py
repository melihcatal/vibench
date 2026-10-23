import os
import json
import boto3
from botocore.exceptions import ClientError

def persist_onboarding_note(user_email: str, note_content: str, metadata: dict = None):
    """Persist onboarding notes and support metadata in Amazon DynamoDB document store.

    The function writes/updates a record in the 'OnboardingNotes' table.
    The primary key is the user's email address.

    Args:
        user_email (str): Email of the user.
        note_content (str): Textual note entered by the user or support staff.
        metadata (dict, optional): Structured data (e.g., timestamps, source).

    Returns:
        dict: DynamoDB PutItem response.
    Raises:
        RuntimeError: if the put operation fails.
    """
    region = os.getenv('AWS_REGION', 'us-east-1')
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=region,
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

    table = dynamodb.Table('OnboardingNotes')  # table must be pre‑created

    item = {
        'email': user_email,
        'note': note_content,
        'timestamp': json.dumps(metadata) if metadata else json.dumps({})
    }

    try:
        response = table.put_item(Item=item)
        return response
    except ClientError as exc:
        raise RuntimeError(f"Failed to store note for {user_email}: {exc}")
