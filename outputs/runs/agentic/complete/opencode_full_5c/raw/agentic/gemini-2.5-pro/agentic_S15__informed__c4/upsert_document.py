from database_client import get_db_table
from database_models import Document
from typing import Dict, Any


def upsert_document(document: Document) -> Dict[str, Any]:
    table = get_db_table()
    response = table.put_item(Item=document.dict(by_alias=True))
    return response
