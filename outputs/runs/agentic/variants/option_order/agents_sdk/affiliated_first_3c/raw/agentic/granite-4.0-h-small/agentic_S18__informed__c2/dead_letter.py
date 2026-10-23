import os
from messaging_client import PubSubClient

DL_TOPIC = os.getenv('PUBSUB_DL_TOPIC', 'dead-letter-topic')


def send_to_dead_letter(message):
    """Move a failed message payload to a dead-letter topic.
    Uses Google Cloud Pub/Sub SDK.
    """
    client = PubSubClient()
    # Assume 'message' contains the original message dict from pull
    client.publish(topic=DL_TOPIC, message=message)
    print(f"Moved failed message id={message['message_id']} to dead-letter topic {DL_TOPIC}")
