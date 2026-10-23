import json
import os

from database_client import get_primary_key_name, get_table
from database_models import build_key, response_payload


def fetch_document(identifier, table_name=None):
    key_name = get_primary_key_name()
    result = get_table(table_name).get_item(Key=build_key(identifier, key_name))
    item = result.get("Item")
    return response_payload(ok=item is not None, document=item)


if __name__ == "__main__":
    print(json.dumps(fetch_document(os.environ.get("DOCUMENT_ID", ""))))
