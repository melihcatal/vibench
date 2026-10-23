import os
from typing import Dict, Any, List

from database_client import get_firestore_client
from database_models import DocumentResponse


def summarize_records(docs: List[DocumentResponse]) -> Dict[str, Any]:
    """Summarize a list of retrieved Firestore documents.

    Args:
        docs: List of DocumentResponse objects (each containing normalized data).
    Returns:
        A concise summary dict with aggregate information.
    """
    summary = {
        "record_count": len(docs),
        "fields": {},  # aggregated distinct field names across docs
        "field_examples": {},  # first sample value per field (for preview)
    }

    for doc in docs:
        data = doc.to_dict()
        summary["field_examples"].update(
            {k: v for k, v in data.items() if k not in summary["field_examples"]}
        )
        for k in data:
            summary["fields"].setdefault(k, set()).add(k)

    # Reduce set to sorted list for readability.
    summary["fields"] = sorted(summary["fields"].keys())
    return summary
