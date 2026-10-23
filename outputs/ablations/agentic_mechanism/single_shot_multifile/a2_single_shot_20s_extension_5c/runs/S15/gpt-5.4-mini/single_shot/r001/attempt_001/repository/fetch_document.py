import json
import os
from typing import Any, Dict

from database_client import get_document_table
from database_models import FetchDocumentRequest, FetchDocumentResponse, normalize_document_from_item


TABLE = get_document_table()


def fetch_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = FetchDocumentRequest.from_dict(payload)
    key = {request.primary_key_name: request.primary_key_value}
    resp = TABLE.get_item(Key=key, ConsistentRead=True)
    item = resp.get("Item")
    document = normalize_document_from_item(item) if item else None
    return FetchDocumentResponse(document=document, found=document is not None).to_dict()


if __name__ == "__main__":
    import sys

    raw = sys.stdin.read() if not sys.stdin.isatty() else os.environ.get("DOCUMENT_JSON", "{}")
    result = fetch_document(json.loads(raw or "{}"))
    print(json.dumps(result))