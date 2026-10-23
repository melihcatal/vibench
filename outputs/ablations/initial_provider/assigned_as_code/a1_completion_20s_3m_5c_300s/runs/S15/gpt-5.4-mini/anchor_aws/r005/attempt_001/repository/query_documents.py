from database_client import get_dynamodb_table, load_database_config
from database_models import document_from_item


def query_documents(payload, config=None):
    config = load_database_config(config)
    table = get_dynamodb_table(config)
    field = payload.get("field", config.get("key_field", "id"))
    value = payload.get("value")
    response = table.scan(FilterExpression=None) if field == config.get("key_field", "id") and value is None else table.scan()
    items = response.get("Items", [])
    if value is not None:
        items = [item for item in items if item.get(field) == value]
    return {"documents": [document_from_item(item) for item in items]}
