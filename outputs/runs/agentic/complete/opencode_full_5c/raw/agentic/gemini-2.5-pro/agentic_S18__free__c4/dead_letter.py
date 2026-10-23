import json
from messaging_client import get_publisher_client, dead_letter_topic_path


def send_to_dead_letter(failed_message: dict, reason: str):
    """Sends a failed message to the dead-letter topic with a reason attribute."""
    publisher = get_publisher_client()

    future = publisher.publish(
        dead_letter_topic_path,
        json.dumps(failed_message).encode("utf-8"),
        reason=reason,
    )

    return future.result()
