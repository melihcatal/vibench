import os
import google.cloud.pubsub_v1 as pubsub

# Google Cloud Pub/Sub credentials via GOOGLE_APPLICATION_CREDENTIALS
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

destination_topic = os.getenv('DEAD_LETTER_TOPIC')  # Topic where failed messages are re‑published


def dead_letter(original_message: dict, error_reason: str) -> None:
    """Move a failed message to a dead‑letter destination (another Pub/Sub topic).

    Args:
        original_message (dict): The original JSON payload that could not be
                                  processed further.
        error_reason (str): Human‑readable description of why processing failed.
    """
    publisher = pubsub.PublisherClient()
    dl_topic_path = publisher.topic_path(project_id, destination_topic)
    # Include original payload and an error field in the dead‑letter message
    dl_payload = {
        **original_message,
        "error": error_reason,
    }
    data = json.dumps(dl_payload).encode('utf-8')
    future = publisher.publish(dl_topic_path, data=data)
    try:
        result = future.result()
        print(f"Dead‑lettered message with ID: {result}")
    except Exception as e:
        print(f"Failed to dead‑letter message: {e}")
