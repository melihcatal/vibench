import os
import boto3
from boto3.dynamodb.conditions import Attr

def summarize_onboarding(user_id: str) -> dict:
    """Summarize onboarding state for support using DynamoDB.
    Returns a dict with user ID, profile status, and notes count.
    """
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'))
    table = dynamodb.Table(os.getenv('ONBOARDING_TABLE_NAME'))
    # Fetch user profile item (status, locale, etc.)
    profile_resp = table.get_item(Key={'userId': user_id})
    profile = profile_resp.get('Item', {})
    # Count notes stored in a separate Notes table (assumed same key schema)
    notes_table = dynamodb.Table(os.getenv('ONBOARDING_NOTES_TABLE_NAME'))
    notes_resp = notes_table.query(KeyConditionExpression=Attr('userId').eq(user_id))
    notes_count = notes_resp.get('Items', [])
    return {
        'userId': user_id,
        'profileStatus': profile.get('status', 'pending'),
        'notesCount': len(notes_resp.get('Items', []))
    }
