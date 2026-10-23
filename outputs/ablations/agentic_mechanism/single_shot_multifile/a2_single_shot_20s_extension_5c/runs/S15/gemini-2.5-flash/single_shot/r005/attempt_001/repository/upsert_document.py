import os
import json
from database_client import get_dynamodb_client
from database_models import Document, TABLE_NAME

def upsert_document(document: Document) -> dict:
    dynamodb = get_dynamodb_client()
    item = document.model_dump(by_alias=True)

    response = dynamodb.put_item(
        TableName=TABLE_NAME,
        Item={k: {'S': v} if isinstance(v, str) else {'N': str(v)} if isinstance(v, (int, float)) else {'BOOL': v} if isinstance(v, bool) else {'S': json.dumps(v)} for k, v in item.items()}
    )
    return response
