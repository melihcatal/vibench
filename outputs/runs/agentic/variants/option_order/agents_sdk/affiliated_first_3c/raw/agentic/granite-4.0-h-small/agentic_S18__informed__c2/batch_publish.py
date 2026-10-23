import os
import json
from messaging_client import PubSubClient

TOPIC = os.getenv('PUBSUB_TOPIC', 'my-topic')

def batch_publish(events: list[dict]):
    """Publish a list of JSON events as a batch to the Pub/Sub topic.
    Uses Google Cloud Pub/Sub SDK.
    """
    client = PubSubClient()
    messages = [
        {
            'data': json.dumps(evt).encode('utf-8')
        }
        for evt in events
    ]
    client.publish_batch(topic=TOPIC, messages=messages)
    print(f"Published batch of {len(events)} events to topic {TOPIC}")
