import json
import os

from database_client import get_table
from database_models import normalize_document, make_response


def upsert_document(document):
    item = normalize_document(document)
    table = get_table()
    table.put_item(Item=item)
    return make_response(True, data=item)


if __name__ == "__main__":
    payload = json.loads(os.environ.get("DOCUMENT_JSON", "{}"))
    print(json.dumps(upsert_document(payload)))
