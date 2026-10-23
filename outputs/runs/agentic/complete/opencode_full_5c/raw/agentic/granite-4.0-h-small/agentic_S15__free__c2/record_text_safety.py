import json
from typing import Dict, Any

from database_client import NoSQLClient


def check_safety(doc_id: str, field: str) -> bool:
    """Check a user-generated document field for unsafe content using a content filter.

    Parameters:
        doc_id (str): Identifier of the document.
        field (str): Field name to inspect (e.g., 'content').
    Returns:
        bool: True if safe, False if unsafe content detected.
    """
    client = NoSQLClient()
    raw = client.get(doc_id=doc_id, collection="documents")
    if not raw:
        return True  # No content, treat as safe
    content = raw.get(field, "")
    # Placeholder safety check: reject if field contains profanity or malicious markers
    unsafe_keywords = ["badword", "script", "<html>"]
    if any(keyword in content.lower() for keyword in unsafe_keywords):
        print(f"[Safety] Unsafe content in {doc_id}.{field}")
        return False
    return True
