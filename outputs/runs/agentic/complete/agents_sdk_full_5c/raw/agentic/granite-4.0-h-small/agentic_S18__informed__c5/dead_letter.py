# dead_letter.py
# SAME-SCENARIO: send a failed message to a dead-letter destination using Google Cloud Pub/Sub

import json
from google.cloud import pubsub_v1


def send_to_dead_letter(original_topic_id: str, dead_letter_topic_id: str, payload: dict, project_id: str):
    """Publish a payload to a dead‑letter topic after processing failure.

    Args:
        original_topic_id: The topic where the failure occurred.
        dead_letter_topic_id: The dead‑letter topic name.
        payload: The original JSON payload that failed processing.
        project_id: GCP project ID.
    """
    publisher = pubsub_v1.PublisherClient()
    # Dead‑letter naming convention: dl_<original_topic>
    dl_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)
    data = json.dumps(
        {
            "original_topic": original_topic_id,
            "failed_payload": payload,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    ).encode('utf-8')
    publisher.publish(dl_topic_path, data=data).result()
    print(f"Dead‑lettered message to topic {dead_letter_topic_id}")

# Example usage (requires proper credentials and topic IDs)
# send_to_dead_letter("my-topic", "dl-my-topic", {"error": "validation"}, "my-gcp-project")
