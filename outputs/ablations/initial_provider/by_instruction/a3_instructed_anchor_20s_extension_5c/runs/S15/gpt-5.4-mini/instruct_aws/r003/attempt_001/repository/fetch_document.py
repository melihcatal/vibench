from typing import Any, Dict, Optional

from database_client import documents_table
from database_models import FetchResponse, normalize_key


def fetch_document(document_id: Any) -> FetchResponse:
    item = documents_table().get_item(Key={"id": normalize_key(document_id)}).get("Item")
    return FetchResponse(document=item)
