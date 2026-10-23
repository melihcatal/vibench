import os
from typing import Dict, Any
from database_client import get_table
from database_models import Document, UpsertResponse

def upsert_document(identifier: str, document: Dict[str, Any]) -> UpsertResponse:
    table = get_table()
    item: Document = {'id': identifier, **document}
    table.put_item(Item=item)
    return item
