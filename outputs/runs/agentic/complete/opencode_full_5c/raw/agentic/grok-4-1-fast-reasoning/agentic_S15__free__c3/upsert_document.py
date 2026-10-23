from database_client import get_table
from database_models import DocumentDict
from typing import Dict, Any


def upsert_document(
    table_name: str, doc_id: str, document: DocumentDict, version: int = 0
):
    table = get_table(table_name)
    item = {"id": doc_id, "data": document, "version": version}
    table.put_item(Item=item)
