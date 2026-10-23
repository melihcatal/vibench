import json
from google.api_core import exceptions
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import normalize_message_payload

def batch_publish(messages, config=None):
    config = config or {}
    publisher = get_publisher_client()
    topic_id = config["topic_id"]
    topic_path = get_topic_path(publisher, topic_id)

    publish_futures = []
    for message_payload in messages:
        event_data = normalize_message_payload(message_payload["event"])
        attributes = message_payload.get("attributes", {})
        publish_futures.append(publisher.publish(topic_path, event_data, **attributes))

    results = []
    for future in publish_futures:
        try:
            message_id = future.result(timeout=30)
            results.append({"message_id": message_id})
        except exceptions.GoogleAPICallError as e:
            print(f"Error publishing message: {e}")
            results.append({"error": str(e)})
    
    publisher.stop()
    return {"published_messages": results}
