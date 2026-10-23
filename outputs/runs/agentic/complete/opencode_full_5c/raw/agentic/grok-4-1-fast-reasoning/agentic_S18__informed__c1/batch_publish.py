import os
from google.cloud import pubsub_v1
from messaging_client import topic_path
from messaging_models import Event, serialize_event

publisher = pubsub_v1.PublisherClient(
    batch_settings=pubsub_v1.types.BatchSettings(
        max_messages=100, max_bytes=100 * 1024, max_latency=1.0
    )
)


def batch_publish(events: list[Event]):
    futures = [
        publisher.publish(topic_path, serialize_event(event)) for event in events
    ]
    for future in futures:
        future.result()
    print(f"Published batch of {len(events)} events")
