import json
from messaging_client import get_messaging_client


def batch_publish(topic, messages, batch_key="batch"):
    """Publish a batch of messages to a managed topic with IDs and attributes.

    Uses Google Cloud Pub/Sub via the google-cloud-pubsub SDK.
    Required environment variable:
        GOOGLE_APPLICATION_CREDENTIALS
    Each item in `messages` should be a dict with at least a 'payload' key.
    Additional keys can serve as attributes.
    Returns the list of message futures.
    """
    client = get_messaging_client()
    publisher = client.publisher_client
    future_list = []
    for idx, msg in enumerate(messages):
        # Use message ID or generate one (Pub/Sub message IDs are immutable)
        message_id = msg.get("id") or f"{batch_key}_{idx}"
        # Build attributes from the item (excluding payload)
        attributes = {k: str(v) for k, v in msg.items() if k != "payload"}
        # Publish the JSON payload
        future = publisher.publish(
            topic_name=topic,
            data=json.dumps(msg["payload"]).encode("utf-8"),
            message_id=message_id,
            attributes=attributes,
        )
        future_list.append(future)
    return future_list
