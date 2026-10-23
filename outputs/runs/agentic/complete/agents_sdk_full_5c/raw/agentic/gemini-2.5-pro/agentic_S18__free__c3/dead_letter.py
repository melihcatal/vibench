import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client

def send_to_dead_letter_topic(failed_message_data: dict, reason: str):
    """
    Publishes a message that failed processing to a designated dead-letter topic.
    
    Note: This simulates application-level dead-lettering. Google Cloud Pub/Sub
    also supports automatic dead-lettering via subscription configuration.
    """
    project_id = os.environ["GCP_PROJECT_ID"]
    dead_letter_topic_id = os.environ["GCP_DEAD_LETTER_TOPIC_ID"]
    
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, dead_letter_topic_id)
    
    # Add failure reason to the message attributes
    attributes = {"failure_reason": reason}
    data = json.dumps(failed_message_data).encode("utf-8")
    
    future = publisher.publish(topic_path, data, **attributes)
    message_id = future.result()
    print(f"Message {message_id} sent to dead-letter topic {dead_letter_topic_id} due to: {reason}")
    return message_id

if __name__ == '__main__':
    if os.getenv("GCP_PROJECT_ID") and os.getenv("GCP_DEAD_LETTER_TOPIC_ID"):
        bad_message = {
            "payload": "invalid_data",
            "error": "Missing required fields"
        }
        send_to_dead_letter_topic(bad_message, "SchemaValidationFail")
    else:
        print("Set GCP_PROJECT_ID and GCP_DEAD_LETTER_TOPIC_ID to run.")
