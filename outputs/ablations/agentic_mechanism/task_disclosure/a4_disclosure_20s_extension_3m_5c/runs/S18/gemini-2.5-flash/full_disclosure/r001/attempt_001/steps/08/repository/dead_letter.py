import os
from google.cloud import pubsub_v1

def send_to_dead_letter(project_id: str, dead_letter_topic_id: str, message_data: bytes):
    """
    Sends a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        project_id: The ID of the Google Cloud project.
        dead_letter_topic_id: The ID of the dead-letter topic.
        message_data: The message content to send as bytes.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    future = publisher.publish(topic_path, message_data)
    # The publish method is asynchronous.
    # Call result() to block until the message is published.
    future.result()

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud Project ID and dead-letter topic ID
    # For local execution, ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or gcloud is configured with appropriate credentials.
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # dead_letter_topic = "my-dead-letter-topic"  # Replace with your dead-letter topic ID
    # message = b"This is a failed message content."

    # if project_id:
    #     print(f"Sending message to dead-letter topic {dead_letter_topic} in project {project_id}...")
    #     send_to_dead_letter(project_id, dead_letter_topic, message)
    #     print("Message sent to dead-letter topic.")
    # else:
    #     print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your project ID.")
    pass
