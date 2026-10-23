import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError

from database_client import get_document_table
from database_models import UpsertDocumentRequest, UpsertDocumentResponse, normalize_document, to_dynamodb_item


TABLE = get_document_table()


def upsert_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = UpsertDocumentRequest.from_dict(payload)
    document = normalize_document(request.document)
    item = to_dynamodb_item(document)
    TABLE.put_item(Item=item)
    return UpsertDocumentResponse(document=document, stored=True).to_dict()


if __name__ == "__main__":
    import sys

    raw = sys.stdin.read() if not sys.stdin.isatty() else os.environ.get("DOCUMENT_JSON", "{}")
    result = upsert_document(json.loads(raw or "{}"))
    print(json.dumps(result))