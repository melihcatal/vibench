import os
import boto3
from datetime import datetime


def persist_onboarding_note(user_id: str, note_content: str, author: str):
    dynamodb = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION"))
    table_name = os.environ["DYNAMODB_NOTES_TABLE"]
    table = dynamodb.Table(table_name)

    timestamp = datetime.utcnow().isoformat()

    item = {
        "userId": user_id,
        "timestamp": timestamp,
        "note": note_content,
        "author": author,
    }

    table.put_item(Item=item)

    return item
