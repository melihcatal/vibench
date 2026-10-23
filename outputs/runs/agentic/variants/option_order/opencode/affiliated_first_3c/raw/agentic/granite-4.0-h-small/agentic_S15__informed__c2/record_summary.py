import json
from typing import List, Dict, Any


def summarize_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a concise summary of a list of NoSQL documents.

    Returns a dict containing counts, sample fields, and pagination hints.
    """
    summary = {"total": len(records), "samples": [], "metadata": {}}
    # Add sample documents (first 3) with only key fields
    for rec in records[:3]:
        sample = {k: rec[k] for k in ("id", "created_at", "status") if k in rec}
        summary["samples"].append(sample)
    # Basic pagination info
    summary["metadata"]["page_size"] = len(records)
    return summary
