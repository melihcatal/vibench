import os
import json
import google.cloud.pubsub_v1 as pubsub

# Google Cloud Pub/Sub credentials via GOOGLE_APPLICATION_CREDENTIALS
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
topic_name = os.getenv('PUBSUB_TOPIC_NAME')

def batch_publish(events: list[dict]) -> list[str]:
    """Publish a list of events (JSON payloads) to a single Pub/Sub topic.

    Args:
        events (list[dict]): Each dict is the payload for one message.
    
    Returns:
        list[str]: The message IDs returned by Pub/Sub for each published
                   event (in the same order as `events`).
    """
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    message_ids = []
    for event in events:
        data = json.dumps(event).encode('utf-8')
        future = publisher.publish(topic_path, data=data)
        try:
            msg_id = future.result()
            message_ids.append(msg_id)
        except Exception as e:
            print(f"Error publishing one of the batch events: {e}")
    return message_ids
