import os
import json
from messaging_client import PubSubClientHelper
from messaging_models import EventMessage

def publish_event(event: EventMessage) -> str:
    client_helper = PubSubClientHelper()
    publisher = client_helper.get_publisher_client()
    topic_id = os.environ.get("GCP_PUBSUB_TOPIC_ID")
    if not topic_id:
        raise ValueError("GCP_PUBSUB_TOPIC_ID environment variable not set.")

    topic_path = client_helper.get_topic_path(topic_id)

    data = json.dumps(event['data']).encode("utf-8")
    attributes = event.get('attributes', {})
    attributes['event_id'] = event['event_id']

    future = publisher.publish(topic_path, data, **attributes)
    message_id = future.result()

    return message_id
