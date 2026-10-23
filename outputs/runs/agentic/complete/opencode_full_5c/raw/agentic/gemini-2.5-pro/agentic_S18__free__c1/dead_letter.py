import os
import json
from messaging_client import get_pubsub_publisher_client
from messaging_models import MessagePayload


def send_to_dead_letter(
    project_id: str,
    dead_letter_topic_id: str,
    failed_message: MessagePayload,
    reason: str,
):
    publisher = get_pubsub_publisher_client()
    topic_path = publisher.topic_path(project_id, dead_letter_topic_id)
    data = failed_message.model_dump_json().encode("utf-8")

    future = publisher.publish(topic_path, data, failure_reason=reason)
    return future.result()
