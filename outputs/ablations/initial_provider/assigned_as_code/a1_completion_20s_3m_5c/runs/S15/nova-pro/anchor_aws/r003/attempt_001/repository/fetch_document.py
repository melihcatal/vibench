import json
from decimal import Decimal

from.database_client import get_dynamodb_client


def fetch_document(document_id, config=None):
    config = config or {}
    client = get_dynamodb_client(config)
    response = client.get_item(
        TableName=config["table_name"],
        Key={config.get("key_field", "id"): {"S": document_id}}
    )
    item = response.get("Item")
    if item:
        return json.loads(json.dumps(item, default=str))
    return None