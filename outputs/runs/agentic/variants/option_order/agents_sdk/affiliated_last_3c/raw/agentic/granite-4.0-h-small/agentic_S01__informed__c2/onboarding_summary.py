import os
import json
import boto3
from boto3.dynamodb.conditions import Attr

# -------------------------------------------------
# Summarize onboarding state for support using DynamoDB
# -------------------------------------------------

def summarize_onboarding(user_email: str) -> dict:
    """Create a concise summary of a user's onboarding journey.

    The function reads user metadata from DynamoDB and returns a
    dict containing creation timestamp, locale, profile moderation flag,
    and any saved onboarding notes.

    Args:
        user_email (str): User's email address (used as primary key).

    Returns:
        dict: Summary with keys: created_at, locale, profile_moderated,
              notes (list). If the user record is missing, returns empty dict.
    """
    region = os.getenv('AWS_REGION', 'us-east-1')
    dynamodb = boto3.resource('dynamodb', region_name=region,
                              aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                              aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    table = dynamodb.Table('OnboardingMetadata')  # must exist

    try:
        response = table.get_item(Key={'email': user_email})
        item = response.get('Item')
        if not item:
            return {}
        summary = {
            'created_at': item.get('created_at'),
            'locale': item.get('locale'),
            'profile_moderated': item.get('profile_moderated', False),
            'notes': item.get('notes', []),
        }
        return summary
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch onboarding metadata for {user_email}: {exc}")
