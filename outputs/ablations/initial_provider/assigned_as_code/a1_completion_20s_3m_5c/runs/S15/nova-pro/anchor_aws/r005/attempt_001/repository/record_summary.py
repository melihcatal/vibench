from database_client import get_table
from database_models import normalize_document


def record_summary(id, config):
    table = get_table(config)
    response = table.get_item(Key={config["key_field"]: id})
    item = response.get("Item")
    if item:
        return normalize_document(item)
    return None