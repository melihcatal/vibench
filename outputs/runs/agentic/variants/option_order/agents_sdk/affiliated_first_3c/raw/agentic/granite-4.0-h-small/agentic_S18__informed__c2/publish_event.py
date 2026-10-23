import os
import json
from messaging_client import PubSubClient

# Configure topic name from environment
TOPIC = os.getenv('PUBSUB_TOPIC', 'my-topic')

def publish_event(event_data: dict, message_id: str = None):
    """Publish a single JSON event to the Pub/Sub topic.
    Uses Google Cloud Pub/Sub SDK.
    """
    client = PubSubClient()
    message = {
        'data': json.dumps(event_data).encode('utf-8'),
        'attributes': {
            'message_id': message_id or str(hash(json.dumps(event_data)))
        }
    }
    client.publish(topic=TOPIC, message=message)
    print(f"Published event (id={message['attributes']['message_id']}) to topic {TOPIC}")
