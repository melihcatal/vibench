import json
from google.api_core import exceptions
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import normalize_message_payload

def dead_letter(payload, config=None):
    config = config or {}
    publisher = get_publisher_client()
    dead_letter_topic_id = config.get("dead_letter_topic_id")

    if not dead_letter_topic_id:
        raise ValueError("dead_letter_topic_id must be provided in config.")

    topic_path = get_topic_path(publisher, dead_letter_topic_id)

    event_data = normalize_message_payload(payload["event"])
    attributes = payload.get("attributes", {})

    try:
        future = publisher.publish(topic_path, event_data, **attributes)
        message_id = future.result(timeout=30)
        return {"dead_letter_message_id": message_id}
    except exceptions.GoogleAPICallError as e:
        print(f"Error publishing to dead-letter topic: {e}")
        return {"error": str(e)}
    finally:
        publisher.stop()
