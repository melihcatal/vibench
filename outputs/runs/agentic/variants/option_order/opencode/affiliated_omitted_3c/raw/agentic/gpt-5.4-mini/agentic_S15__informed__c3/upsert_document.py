import json
import os

from database_client import get_primary_key_name, get_table
from database_models import normalize_document, response_payload


def upsert_document(document, table_name=None):
    item = normalize_document(document)
    key_name = get_primary_key_name()
    if key_name not in item:
        raise ValueError(f"Missing primary identifier: {key_name}")
    get_table(table_name).put_item(Item=item)
    return response_payload(ok=True, document=item)


if __name__ == "__main__":
    raw = os.environ.get("DOCUMENT_JSON", "{}")
    print(json.dumps(upsert_document(raw)))
