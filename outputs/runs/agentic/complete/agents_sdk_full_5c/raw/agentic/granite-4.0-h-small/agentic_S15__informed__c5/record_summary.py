from typing import List, Dict
from database_models import Document

# Placeholder: summarize fetched documents (e.g., aggregate, key figures)

def summarize_documents(docs: List[Document]) -> Dict[str, Any]:
    """Generate a high-level summary of a list of document records."""
    count = len(docs)
    keys = set().union(*(d["data"].keys() for d in docs))
    summary = {
        "count": count,
        "fields": sorted(keys),
        "sample": docs[:2] if docs else None,
    }
    return summary
