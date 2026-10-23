import json
import os

from database_client import get_table
from database_models import make_response


def fetch_document(document_id):
    table = get_table()
    result = table.get_item(Key={"document_id": document_id})
    item = result.get("Item")
    if not item:
        return make_response(False, error="not_found")
    return make_response(True, data=item)


if __name__ == "__main__":
    print(json.dumps(fetch_document(os.environ.get("DOCUMENT_ID", ""))))
