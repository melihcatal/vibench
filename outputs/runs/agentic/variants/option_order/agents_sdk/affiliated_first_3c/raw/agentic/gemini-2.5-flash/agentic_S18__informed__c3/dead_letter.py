from google.cloud import pubsub_v1
import os
import json

def send_to_dead_letter_topic(project_id: str, dead_letter_topic_id: str, failed_message_data: dict, attributes: dict = None):
    """Sends a failed message to a specified dead-letter topic in Google Cloud Pub/Sub.
    In a real scenario, this would typically be handled by Pub/Sub's dead-lettering feature
    configured on the subscription, but this function demonstrates explicit publishing.
    """
    publisher = pubsub_v1.PublisherClient()
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)
    
    message_json = json.dumps(failed_message_data).encode("utf-8")
    
    future = publisher.publish(dead_letter_topic_path, message_json, **(attributes or {}))
    print(f"Sent to dead-letter topic (message ID: {future.result()})")

if __name__ == '__main__':
    # Example usage
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    DEAD_LETTER_TOPIC_ID = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "my-dead-letter-topic")
    
    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        failed_payload = {"original_message": "This message failed processing", "error": "Invalid format"}
        error_attributes = {"reason": "processing_failure", "original_id": "msg-12345"}
        send_to_dead_letter_topic(PROJECT_ID, DEAD_LETTER_TOPIC_ID, failed_payload, error_attributes)
