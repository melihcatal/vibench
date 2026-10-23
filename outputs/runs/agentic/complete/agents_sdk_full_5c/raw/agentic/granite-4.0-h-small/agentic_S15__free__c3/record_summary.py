# record_summary.py
# [LATER-STEP] Summarize a fetched Azure Cosmos DB document record

from typing import Optional, Dict

def summarize_record(record: Optional[Dict[str, any]]) -> str:
    """Create a concise one‑line summary of the given document."""
    if not record:
        return "No record found"
    # Use common fields: title, description, status
    title = record.get("title", "<no title>")
    status = record.get("status", "<no status>")
    created = record.get("created_at", "<no date>")
    return f"Title: '{title}' | Status: {status} | Created: {created}"
