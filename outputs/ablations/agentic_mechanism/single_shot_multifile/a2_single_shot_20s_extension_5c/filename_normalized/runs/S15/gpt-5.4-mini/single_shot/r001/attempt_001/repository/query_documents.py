import json
import os
from typing import Any, Dict

from boto3.dynamodb.conditions import Attr, Key

from database_client import get_document_table
from database_models import QueryDocumentsRequest, QueryDocumentsResponse, normalize_document_from_item


TABLE = get_document_table()


def query_documents(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = QueryDocumentsRequest.from_dict(payload)
    if request.partition_key_name and request.partition_key_value is not None:
        resp = TABLE.query(KeyConditionExpression=Key(request.partition_key_name).eq(request.partition_key_value))
    elif request.field_name and request.field_value is not None:
        resp = TABLE.scan(FilterExpression=Attr(request.field_name).eq(request.field_value))
    else:
        resp = TABLE.scan()
    documents = [normalize_document_from_item(item) for item in resp.get("Items", [])]
    return QueryDocumentsResponse(items=documents, count=len(documents)).to_dict()


if __name__ == "__main__":
    import sys

    raw = sys.stdin.read() if not sys.stdin.isatty() else os.environ.get("DOCUMENT_JSON", "{}")
    result = query_documents(json.loads(raw or "{}"))
    print(json.dumps(result))