import json
import os
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError

from database_client import get_table
from database_models import UpsertDocumentRequest, normalize_document


def upsert_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = UpsertDocumentRequest.from_dict(payload)
    table = get_table()
    item = normalize_document(request.document)
    item[request.id_field] = request.document_id
    try:
        table.put_item(Item=item)
    except ClientError as exc:
        raise RuntimeError(f"Failed to upsert document: {exc}") from exc
    return {"ok": True, "id": request.document_id, "table": os.environ.get("DYNAMODB_TABLE", "")}
