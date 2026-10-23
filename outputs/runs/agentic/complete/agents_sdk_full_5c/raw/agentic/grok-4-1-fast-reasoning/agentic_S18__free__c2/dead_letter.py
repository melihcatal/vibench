import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_topic_path

def send_to_dead_letter(failed_message: dict, attributes: dict = None):
    """
    sends failed messages to a dead-letter destination
    """
    dlq_topic = os.getenv('DEAD_LETTER_TOPIC_ID')
    if not dlq_topic:
        raise ValueError('DEAD_LETTER_TOPIC_ID required')
    topic_path = get_topic_path(dlq_topic)
    publisher = pubsub_v1.PublisherClient()
    data = json.dumps(failed_message).encode('utf-8')
    future = publisher.publish(topic_path, data, **(attributes or {}))
    future.result()
    print("Sent to dead-letter queue")