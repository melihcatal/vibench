# batch_publish.py
"""
Same-scenario scored implementation: batch_publish.py
Provides a function to publish a batch of messages with IDs or attributes to a Pub/Sub topic.
"""

from google.cloud import pubsub_v1
from messaging_models import PubSubConfig
import json


def batch_publish(config: PubSubConfig, messages: list[dict]) -> list[str]:
    """Publish a list of messages to a Pub/Sub topic and return their IDs.

    Args:
        config (PubSubConfig): Configuration with project ID and topic name.
        messages (list[dict]): Each dict represents a message payload;
                               IDs can be added later if needed.

    Returns:
        list[str]: A list of Pub/Sub message IDs in the same order as the input.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(config.project_id, config.topic_name)
    publish_futures = []
    for payload in messages:
        data = json.dumps(payload).encode("utf-8")
        # Publish each message; result() waits for ack
        publish_futures.append(publisher.publish(topic_path, data=data))
    # Collect message IDs (blocking)
    return [f.result() for f in publish_futures]
