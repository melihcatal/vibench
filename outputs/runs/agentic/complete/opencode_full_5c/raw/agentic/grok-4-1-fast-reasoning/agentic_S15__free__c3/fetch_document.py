from typing import Optional
from database_client import get_table
from database_models import DocumentDict


def fetch_document(table_name: str, doc_id: str) -> Optional[DocumentDict]:
    table = get_table(table_name)
    response = table.get_item(Key={"id": doc_id})
    return response.get("Item")
