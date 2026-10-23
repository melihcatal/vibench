import json
import os

from database_client import table
from database_models import fetch_result, normalize_id


def fetch_document(document_id):
    item = table().get_item(Key={"id": normalize_id(document_id)}).get("Item")
    return fetch_result(item)


def main():
    document_id = os.environ.get("DOCUMENT_ID")
    print(json.dumps(fetch_document(document_id)))


if __name__ == "__main__":
    main()
