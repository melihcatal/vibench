import json
from messaging_client import get_publisher_client, get_dead_letter_topic_path


def send_to_dead_letter(failed_message_data: dict):
    publisher = get_publisher_client()
    dead_letter_topic_path = get_dead_letter_topic_path()

    data = json.dumps(failed_message_data).encode("utf-8")

    future = publisher.publish(dead_letter_topic_path, data)
    return future.result()
