import json
from typing import Any, Dict

from database_client import get_container
from database_models import UpsertDocumentRequest


def upsert_document(document_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
    container = get_container()
    req = UpsertDocumentRequest(id=document_id, document=document)
    return container.upsert_item(req.to_item())


def main(payload: str) -> str:
    data = json.loads(payload)
    result = upsert_document(data["id"], data.get("document", {}))
    return json.dumps(result)
