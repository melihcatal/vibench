import json

from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import create_message_payload

def batch_publish(messages, config=None):
    config = config or {}
    publisher = get_publisher_client()
    topic_path = get_topic_path(publisher, config["topic_id"])

    futures = []
    for msg in messages:
        # Each msg in the batch is expected to have 'event_data' and optionally 'attributes'
        event_data = msg.get("event_data", {})
        attributes = msg.get("attributes", {})
        
        message = create_message_payload(event_data, attributes)
        future = publisher.publish(topic_path, message["data"], **message["attributes"])
        futures.append(future)

    results = []
    for future in futures:
        try:
            results.append({"message_id": future.result(timeout=30)})
        except Exception as e:
            results.append({"error": str(e)})
    
    publisher.stop()
    return results
