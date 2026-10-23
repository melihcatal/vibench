import json
from database_models import normalize_item

def summarize_document(item: dict) -> str:
    """Generate a concise human‑readable summary of a DynamoDB document.
    Normalizes the raw item and extracts a few key fields.
    """
    normalized = normalize_item(item)
    # Example summary: combine id, title, and a short excerpt
    summary_parts = []
    summary_parts.append(f'ID: {normalized.get("id")}')
    summary_parts.append(f'Title: {normalized.get("title")}')
    excerpt = normalized.get("content")
    if excerpt and len(excerpt) > 100:
        excerpt = excerpt[:100] + '...'
    summary_parts.append(f'Content snippet: {excerpt}')
    return ' | '.join(summary_parts)
