# [HELPER] database_models.py

from typing import Dict, Any

# Example schema for a document record
Document = Dict[str, Any]

# Local function to normalize incoming payload
# Before sending to the managed store


def normalize_document(doc: Document) -> Document:
    """Ensure required keys exist and coerce types.

    Args:
        doc (Document): Incoming document dictionary.

    Returns:
        Document: Normalized dict ready for storage.
    """
    # Example: ensure 'id' is a string primary key
    doc["id"] = str(doc.get("id", ""))
    # Example: enforce string type for 'timestamp'
    doc["timestamp"] = str(doc.get("timestamp", ""))
    return doc


# Local function to extract needed fields for API response


def extract_response(doc: Document) -> Document:
    """Return a sanitized version of the document for clients.

    Args:
        doc (Document): Full document from the store.

    Returns:
        Document: Response-ready dictionary.
    """
    # Omit internal fields like '__meta__'
    return {k: v for k, v in doc.items() if not k.startswith("_")}
