from database_client import get_dynamodb_client
from database_models import Document
import json

def upsert_document(table_name: str, document: Document):
    dynamodb = get_dynamodb_client()
    item = document.to_item()
    response = dynamodb.put_item(
        TableName=table_name,
        Item=json.loads(json.dumps(item), parse_float=str)
    )
    return response
