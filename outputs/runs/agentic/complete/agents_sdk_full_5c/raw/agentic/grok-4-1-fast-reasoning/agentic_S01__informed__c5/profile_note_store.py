import os
import boto3
import time
from typing import Dict, Any

TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'OnboardingNotes')

def store_profile_notes(user_id: str, notes: Dict[str, Any]) -> None:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(
        Item={
            'user_id': user_id,
            'notes': notes,
            'updated_at': int(time.time())
        }
    )