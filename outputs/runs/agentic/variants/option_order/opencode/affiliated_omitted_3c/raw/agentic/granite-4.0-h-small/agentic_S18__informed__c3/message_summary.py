import json
from messaging_models import Event

def summarize_processed(event: Event) -> Dict[str, Any]:
    """Create a concise summary record for processed events.",
    summary = {
        "event_id": event.id if event.id else "unknown",
        "topic": event.topic if hasattr(event, 'topic') else "unknown",
        "processed_at": event.get('event_timestamp', 'unknown'),
        "status": "processed",
    }
    return summary

# Example usage (not executed here)
# ev = Event(json.loads(message['data']))
# print(json.dumps(summarize_processed(ev)))
