import os
from typing import List, Dict
from google.cloud import firestore
from messaging_models import normalize_message

def summarize_processed_messages(batch: List[Dict]) -> Dict:
    """Summarize a batch of normalized messages and store summary in Firestore.

    Args:
        batch (List[Dict]): List of message payloads (already normalized).
    Returns:
        Dict: Summary dict containing counts and timestamps.
    """
    summary = {
        'count': len(batch),
        'earliest': None,
        'latest': None,
        'topics': set()
    }
    for msg in batch:
        # Assume each message has a 'processed_at' timestamp (ISO string)
        ts = msg.get('processed_at')
        try:
            ts_dt = datetime.datetime.fromisoformat(ts)
        except Exception:
            continue
        if summary['earliest'] is None or ts_dt < summary['earliest']:
            summary['earliest'] = ts
        if summary['latest'] is None or ts_dt > summary['latest']:
            summary['latest'] = ts
        # If topic field exists, track it
        summary['topics'].add(msg.get('topic', 'unknown'))
    return summary
