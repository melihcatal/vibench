import datetime

def summarize(message_records):
    """Summarize processed Pub/Sub messages for reporting.
    Expects a list of dicts with at least 'message_id' and 'payload'.
    Returns a dictionary summary.
    """
    summary = {
        'total_messages': len(message_records),
        'processed_at': datetime.datetime.utcnow().isoformat() + 'Z',
        'message_ids': [rec['message_id'] for rec in message_records]
    }
    # Example: count by a business attribute if present
    summary['counts_by_type'] = {}
    for rec in message_records:
        evt_type = rec['payload'].get('event_type')
        if evt_type:
            summary['counts_by_type'][evt_type] = summary['counts_by_type'].get(evt_type, 0) + 1
    return summary
