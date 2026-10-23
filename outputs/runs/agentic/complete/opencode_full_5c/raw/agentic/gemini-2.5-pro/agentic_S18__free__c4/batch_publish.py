import json
from concurrent.futures import as_completed
from messaging_client import get_publisher_client, topic_path


def publish_batch(messages: list):
    """Publishes a batch of messages with attributes to the configured topic."""
    publisher = get_publisher_client()
    publish_futures = []

    for message_data in messages:
        data = message_data.get("data", {})
        attributes = message_data.get("attributes", {})

        future = publisher.publish(
            topic_path, json.dumps(data).encode("utf-8"), **attributes
        )
        publish_futures.append(future)

    # Wait for all the publish futures to resolve
    message_ids = []
    for future in as_completed(publish_futures):
        message_ids.append(future.result())

    return message_ids
