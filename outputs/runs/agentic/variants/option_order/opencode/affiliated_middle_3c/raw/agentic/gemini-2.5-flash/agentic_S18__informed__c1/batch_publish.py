import os
from typing import List, Dict, Any, Optional
from messaging_client import PubSubClient
from messaging_models import EventPayload, PubSubMessage

# Google Cloud Pub/Sub provider-identifying signal: google.cloud.pubsub_v1


def batch_publish_events(topic_id: str, events: List[Dict[str, Any]]) -> List[str]:
    """Publishes a batch of JSON events to a Google Cloud Pub/Sub topic."""
    client = PubSubClient()
    topic_path = client.get_topic_path(topic_id)

    futures = []
    for event in events:
        event_data = event.get("data", {})
        event_type = event.get("event_type", "generic_batch_event")
        source = event.get("source", "batch_publisher")
        event_id = event.get("event_id")

        payload = EventPayload(
            data=event_data, event_type=event_type, source=source, event_id=event_id
        )
        data = payload.to_json_string().encode("utf-8")

        attributes = {"event_type": event_type, "source": source}
        if event_id:
            attributes["event_id"] = event_id

        future = client.publisher.publish(topic_path, data, **attributes)
        futures.append(future)

    # Wait for all messages in the batch to be published
    message_ids = [f.result() for f in futures]
    return message_ids
