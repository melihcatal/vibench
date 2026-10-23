# [LATER-STEP] record_summary.py
import json
from database_client import NoSQLClient
from database_models import denormalize_document

def summarize_documents(doc_ids):
    """Retrieve and summarize a batch of documents.

    Args:
        doc_ids (list): List of document primary IDs.
    Returns:
        list: Summaries containing id, title (or name), and a short excerpt.
    """
    client = NoSQLClient()
    summaries = []
    for doc_id in doc_ids:
        item = client.get_item(TableName=client.table_name, Key={'id': {'S': doc_id}})
        raw = item.get('Item', {})
        if not raw:
            continue
        doc = denormalize_document(json.loads(raw.get('content', '{}')))
        # Build a concise summary
        summary = {
            'id': doc_id,
            'title': doc.get('title', 'No Title'),
            'excerpt': (doc.get('content', '')[:200] + '...') if isinstance(doc.get('content'), str) else ''
        }
        summaries.append(summary)
    return summaries