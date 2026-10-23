from typing import Any, Dict, Optional

from database_client import document_key, table_resource
from database_models import DocumentFetchResponse


def fetch_document(document_id: str, sort_key: Optional[str] = None) -> Dict[str, Any]:
    response = table_resource().get_item(Key=document_key(document_id, sort_key))
    item = response.get("Item")
    result = DocumentFetchResponse(found=item is not None, document=item or {})
    return {"found": result.found, "document": result.document}
