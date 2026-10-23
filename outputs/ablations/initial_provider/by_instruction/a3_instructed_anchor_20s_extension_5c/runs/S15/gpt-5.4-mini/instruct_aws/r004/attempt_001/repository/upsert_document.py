import json
import os

import boto3

from database_client import table
from database_models import normalize_document, normalize_id, upsert_result


def upsert_document(document, primary_id=None):
    payload = normalize_document(document)
    doc_id = normalize_id(primary_id if primary_id is not None else payload.get("id"))
    payload["id"] = doc_id
    table().put_item(Item=payload)
    return upsert_result(payload)


def main():
    body = os.environ.get("DOCUMENT_JSON", "{}")
    primary_id = os.environ.get("DOCUMENT_ID")
    result = upsert_document(body, primary_id)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
