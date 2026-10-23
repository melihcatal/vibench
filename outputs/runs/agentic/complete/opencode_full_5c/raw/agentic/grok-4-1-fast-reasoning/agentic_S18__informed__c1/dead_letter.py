import os
from google.cloud import pubsub_v1
from messaging_client import dl_path, project_id, topic_id
from messaging_models import Event, serialize_event

publisher = pubsub_v1.PublisherClient()


def send_to_dead_letter(event: Event, error_msg: str):
    attributes = {"original_topic": topic_id, "error": error_msg}
    msg_id = publisher.publish(dl_path, serialize_event(event), **attributes).result()
    print(f"Sent to dead letter {event.id} with message ID {msg_id}")
