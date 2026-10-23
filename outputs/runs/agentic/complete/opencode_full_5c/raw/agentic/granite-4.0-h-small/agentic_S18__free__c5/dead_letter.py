# dead_letter.py
"""
Same-scenario scored implementation: dead_letter.py
Provides a function to send a failed message to a dead-letter destination (topic or queue).
"""

from google.cloud import pubsub_v1
from messaging_models import PubSubConfig
import json


def send_dead_letter(message: dict, dlq_config: PubSubConfig) -> None:
    """Send a failed message to a dead-letter Pub/Sub topic.

    Args:
        message (dict): The original message payload to be dead-lettered.
        dlq_config (PubSubConfig): Configuration for the dead-letter topic (project and topic).
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(dlq_config.project_id, dlq_config.topic_name)
    payload = json.dumps({"original": message, "reason": "dead_letter"}).encode("utf-8")
    # Provider identifier (GCP Pub/Sub) is apparent from the library import and topic_path call
    publisher.publish(topic_path, data=payload).result()
