from __future__ import annotations

from database_client import get_documents_table
from database_models import DocumentResponse


def fetch_document(document_id: str) -> dict:
    table = get_documents_table()
    item = table.get_item(Key={"id": str(document_id)}).get("Item")
    response = DocumentResponse.from_item(item)
    return {
        "id": response.id or str(document_id),
        "found": response.found,
        "document": response.document,
        "version": response.version,
    }
