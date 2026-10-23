def summarize(event_data):
    """Generate a high‑level summary of a processed event.",
    summary = {
        "event_id": event_data.get('id'),
        "timestamp": event_data.get('timestamp'),
        "type": event_data.get('type'),
        "status": event_data.get('status', 'unknown'),
        "payload_size_bytes": len(str(event_data).encode('utf-8')),
    }
    return summary
