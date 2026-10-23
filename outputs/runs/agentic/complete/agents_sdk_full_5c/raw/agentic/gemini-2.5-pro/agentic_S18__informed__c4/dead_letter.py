import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_project_id, get_topic_path

def send_to_dead_letter_queue(failed_message_data: bytes, attributes: dict):
    """
    Sends a failed message to a designated dead-letter topic in Google Cloud Pub/Sub.
    """
    project_id = get_project_id()
    dead_letter_topic_id = os.getenv("GCP_PUBSUB_DEAD_LETTER_TOPIC_ID", "my-dead-letter-topic")
    
    publisher = get_publisher_client()
    topic_path = get_topic_path(publisher, project_id, dead_letter_topic_id)

    future = publisher.publish(topic_path, failed_message_data, **attributes)
    
    message_id = future.result()
    print(f"Message {message_id} sent to dead-letter topic {topic_path}.")
    return message_id
