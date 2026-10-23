import os
from google.cloud import pubsub_v1
from messaging_client import topic_path
from messaging_models import Event, serialize_event

publisher = pubsub_v1.PublisherClient()


def publish_event(event: Event):
    msg_id = publisher.publish(topic_path, serialize_event(event)).result()
    print(f"Published event {event.id} with message ID {msg_id}")
