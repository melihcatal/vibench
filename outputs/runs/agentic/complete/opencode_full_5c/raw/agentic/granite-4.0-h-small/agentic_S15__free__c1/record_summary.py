import json
from database_models import DatabaseModels

# Google Cloud Firestore (managed NoSQL) integration helper


def record_summary(record: dict) -> dict:
    """Generate a concise summary of a retrieved document."""
    # Example: return only a few key fields for UI display
    summary = {
        "id": record.get("id"),
        "title": record.get("title"),
        "created_at": record.get("created_at"),
    }
    return summary
