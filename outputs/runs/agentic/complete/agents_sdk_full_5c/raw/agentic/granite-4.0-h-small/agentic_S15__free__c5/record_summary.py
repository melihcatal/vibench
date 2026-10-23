def summarize_record(record: dict) -> dict:
    """Creates a concise summary of a retrieved document record.

    Focuses on high-level fields and hides large textual content for quick overview.
    
    Args:
        record (dict): Full document from NoSQL store.
    
    Returns:
        dict: Summary containing selected fields.
    """
    summary = {
        "id": record.get("_id"),
        "title": record.get("title"),
        "created_at": record.get("created_at"),
        "metadata": {k: v for k, v in record.items() if k not in {"_id", "title", "content", "created_at"}}
    }
    return summary
