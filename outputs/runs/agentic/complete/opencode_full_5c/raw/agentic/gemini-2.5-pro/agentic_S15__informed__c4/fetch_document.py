from database_client import get_db_table
from typing import Dict, Any, Optional


def fetch_document_by_id(doc_id: str) -> Optional[Dict[str, Any]]:
    table = get_db_table()
    response = table.get_item(Key={"doc_id": doc_id})
    return response.get("Item")
