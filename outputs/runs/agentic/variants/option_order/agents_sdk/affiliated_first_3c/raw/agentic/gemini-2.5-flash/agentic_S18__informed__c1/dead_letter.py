import json
import os
from google.cloud import pubsub_v1

def send_to_dead_letter_topic(project_id: str, dead_letter_topic_id: str, failed_message_data: dict, attributes: dict = None):
    """
    Sends a failed message to a Google Cloud Pub/Sub dead-letter topic.
    In a real scenario, this would typically be triggered by a consumer
    that fails to process a message.
    """
    publisher = pubsub_v1.PublisherClient()
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    data = json.dumps(failed_message_data).encode("utf-8")
    
    if attributes is None:
        attributes = {}
    
    future = publisher.publish(dead_letter_topic_path, data, **attributes)
    print(f"Sent message to dead-letter topic {dead_letter_topic_id}. Message ID: {future.result()}")
    return future.result()

if __name__ == "__main__":
    # For demonstration purposes
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    DEAD_LETTER_TOPIC_ID = "my-dead-letter-topic" # Ensure this topic exists

    failed_event = {
        "original_message": {"id": "msg-123", "content": "problematic data"},
        "error": "Processing failed due to invalid format",
        "attempt_count": 3
    }
    failure_attributes = {
        "error_type": "DataValidationError",
        "consumer_id": "consumer-service-A"
    }

    if PROJECT_ID:
        send_to_dead_letter_topic(PROJECT_ID, DEAD_LETTER_TOPIC_ID, failed_event, failure_attributes)
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
