import json
from typing import List, Dict

from database_client import NoSQLClient
from database_models import DocumentResponse


def summarize_documents(doc_ids: List[str]) -> List[Dict[str, Any]]:
    """Summarize retrieved document records by extracting key fields.

    Parameters:
        doc_ids (List[str]): IDs of documents to summarize.
    Returns:
        List[Dict[str, Any]]: Summarized data per document.
    """
    client = NoSQLClient()
    summaries = []
    for doc_id in doc_ids:
        data = client.get(doc_id=doc_id, collection="documents")
        if not data:
            continue
        doc = DocumentResponse(raw=data)
        # Example summary: title, created timestamp, and status field
        summary = {
            "id": doc_id,
            "title": doc.normalized.get("title"),
            "created": doc.normalized.get("createdAt"),
            "status": doc.normalized.get("status"),
        }
        summaries.append(summary)
    return summaries
