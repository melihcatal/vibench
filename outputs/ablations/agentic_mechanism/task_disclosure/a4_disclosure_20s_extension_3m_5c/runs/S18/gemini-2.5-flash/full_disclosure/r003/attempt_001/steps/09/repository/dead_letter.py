from google.cloud import pubsub_v1
import os

def send_to_dead_letter(project_id: str, topic_id: str, message_data: str):
    """Sends a message to a Google Cloud Pub/Sub dead-letter topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    message_bytes = message_data.encode("utf-8")

    try:
        future = publisher.publish(topic_path, message_bytes)
        print(f"Published message ID: {future.result()}")
    except Exception as e:
        print(f"Failed to publish message: {e}")

if __name__ == "__main__":
    # Example usage:
    # Replace with your Google Cloud Project ID and dead-letter topic ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    dead_letter_topic_id = "your-dead-letter-topic-id" 
    
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        print("Please set it to your Google Cloud Project ID.")
    else:
        failed_message_content = "This is a failed message that needs to be dead-lettered."
        send_to_dead_letter(project_id, dead_letter_topic_id, failed_message_content)
