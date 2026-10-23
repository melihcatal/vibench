from database_client import get_table
from database_models import build_response


def fetch_document(payload, config=None):
    table, cfg = get_table(config)
    item = table.get_item(Key={cfg["key_field"]: payload["id"]}).get("Item")
    return build_response(item, id=payload["id"])
