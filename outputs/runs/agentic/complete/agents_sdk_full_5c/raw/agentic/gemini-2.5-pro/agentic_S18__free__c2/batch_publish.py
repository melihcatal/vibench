from typing import List, Dict
from google.cloud import pubsub_v1

from messaging_client import get_publisher_client, get_topic_path, MAIN_TOPIC_ID

def publish_message_batch(messages: List[Dict[str, str]]) -> List[str]:
    """
    Publishes a batch of messages to a Google Cloud Pub/Sub topic.
    Each message in the list should be a dict with 'data' and optional 'attributes'.
    """
    publisher = get_publisher_client()
    topic_path = get_topic_path(MAIN_TOPIC_ID)
    
    futures = []
    
    for message in messages:
        data = message.get("data", "").encode("utf-8")
        attributes = message.get("attributes", {})
        
        future = publisher.publish(topic_path, data, **attributes)
        futures.append(future)
        
    published_ids = []
    for future in futures:
        try:
            message_id = future.result()
            published_ids.append(message_id)
        except Exception as e:
            print(f"An error occurred publishing a message in batch: {e}")
            
    print(f"Successfully published {len(published_ids)} messages in a batch.")
    return published_ids
