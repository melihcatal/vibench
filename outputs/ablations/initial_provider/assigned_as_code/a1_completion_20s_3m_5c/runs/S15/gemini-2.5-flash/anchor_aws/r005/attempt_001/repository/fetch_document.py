import os
from database_client import get_dynamodb_resource
from database_models import normalize_document_from_db

def fetch_document(document_id: str, table_name: str, key_field: str = "id", region_name: str = None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    dynamodb = get_dynamodb_resource(region_name=region_name)
    table = dynamodb.Table(table_name)

    response = table.get_item(Key={key_field: document_id})
    item = response.get("Item")

    if item:
        return normalize_document_from_db(item)
    return None
