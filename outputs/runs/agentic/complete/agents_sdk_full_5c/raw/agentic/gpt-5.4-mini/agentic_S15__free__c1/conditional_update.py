from typing import Any, Dict, Optional

from botocore.exceptions import ClientError

from database_client import document_key, table_resource
from database_models import DocumentConditionalUpdateRequest, DocumentConditionalUpdateResponse, merge_updates


def conditional_update(document_id: str, updates: Dict[str, Any], expected_version: Optional[int] = None, sort_key: Optional[str] = None) -> Dict[str, Any]:
    request = DocumentConditionalUpdateRequest(document_id=document_id, updates=updates, expected_version=expected_version, sort_key=sort_key)
    table = table_resource()
    current = table.get_item(Key=document_key(request.document_id, request.sort_key)).get("Item", {})
    if request.expected_version is not None and current.get("version") != request.expected_version:
        return {"updated": False, "reason": "version_mismatch", "document": current}
    merged = merge_updates(current, request.updates)
    merged["version"] = int(current.get("version", 0)) + 1
    table.put_item(Item=merged)
    response = DocumentConditionalUpdateResponse(updated=True, document=merged)
    return {"updated": response.updated, "document": response.document}
