# message_summary.py
# [LATER-STEP]
# Summarize processing results of a batch of Pub/Sub messages.

from typing import List, Dict
from .messaging_models import EventMessage

def summarize_messages(messages: List[EventMessage]) -> Dict[str, int]:
    """Produce a summary dict for a list of EventMessage objects.

    Returns a dictionary with counts of total, successful, and failed (e.g., DLQ) messages.
    """
    summary = {
        "total": len(messages),
        "successful": 0,
        "dead_lettered": 0,
    }
    for msg in messages:
        # Example heuristic: treat messages with 'dlq_sent': True attribute as dead-lettered
        if msg.attributes.get('dlq_sent', 'false').lower() == 'true':
            summary['dead_lettered'] += 1
        else:
            summary['successful'] += 1
    return summary
