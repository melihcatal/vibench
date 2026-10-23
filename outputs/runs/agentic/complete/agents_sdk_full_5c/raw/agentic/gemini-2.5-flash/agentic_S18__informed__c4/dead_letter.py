from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage

def send_to_dead_letter(dead_letter_topic_id: str, original_message: PubSubMessage, error_details: str):
    publisher = get_publisher_client()
    project_id = get_project_id()
    if not project_id:
        raise ValueError("Google Cloud Project ID not found. Set GOOGLE_CLOUD_PROJECT environment variable.")
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    # Augment attributes for dead-lettering
    attributes = original_message.attributes or {}
    attributes["dlq_reason"] = error_details
    attributes["original_topic"] = "unknown" # In a real scenario, get this from the original message metadata

    data = original_message.data.encode("utf-8")
    future = publisher.publish(dead_letter_topic_path, data, **attributes)
    print(f"Sent message to dead-letter topic. Message ID: {future.result()}")
    return future.result()
