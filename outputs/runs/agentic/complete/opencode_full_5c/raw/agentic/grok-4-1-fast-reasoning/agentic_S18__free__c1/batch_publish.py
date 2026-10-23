from typing import List, Dict, Any

from messaging_client import topic_path, publisher
from messaging_models import serialize_event


def batch_publish(
    events: List[Dict[str, Any]], topic_name: str = "events-topic"
) -> List[str]:
    topic_p = topic_path(topic_name)
    futures = []
    for i, event in enumerate(events):
        data = serialize_event(event)
        future = publisher.publish(
            topic_p,
            data,
            batch_index=str(i),
            event_type=event.get("event_type", "unknown"),
        )
        futures.append(future)
    return [f.result() for f in futures]
