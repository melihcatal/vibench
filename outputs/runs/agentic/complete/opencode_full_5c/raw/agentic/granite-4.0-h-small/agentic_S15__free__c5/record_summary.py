# record_summary.py
# Later-step: Summarize retrieved document records
from typing import List, Dict

from database_models import DocumentResponse


def summarize_documents(documents: List[DocumentResponse]) -> List[Dict[str, str]]:
    """Generate concise summaries for a list of document records.

    Args:
        documents (List[DocumentResponse]): Retrieved documents.

    Returns:
        List[Dict[str, str]]: List of summaries containing key fields.
    """
    summaries = []
    for doc in documents:
        summary = {
            "id": doc.id,
            "type": doc.data.get("type"),  # example field
            "created_at": doc.data.get("created_at"),
        }
        summaries.append(summary)
    return summaries
