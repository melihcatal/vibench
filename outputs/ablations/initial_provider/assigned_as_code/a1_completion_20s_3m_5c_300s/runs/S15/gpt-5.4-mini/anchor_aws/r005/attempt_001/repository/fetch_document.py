from database_client import get_dynamodb_table, load_database_config
from database_models import document_from_item


def fetch_document(payload, config=None):
    config = load_database_config(config)
    table = get_dynamodb_table(config)
    key_field = config.get("key_field", "id")
    response = table.get_item(Key={key_field: payload["id"]})
    item = response.get("Item")
    return {"document": document_from_item(item) if item is not None else None}
