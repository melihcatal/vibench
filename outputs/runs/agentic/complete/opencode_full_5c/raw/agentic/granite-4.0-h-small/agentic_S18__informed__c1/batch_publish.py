import json
from messaging_client import PubSubClient


def batch_publish(topic_name: str, messages: list[dict]) -> None:
    """Publish a batch of JSON messages to a Pub/Sub topic.

    Args:
        topic_name: Topic to publish to.
        messages: List of dictionaries, each representing one message payload.
    """
    client = PubSubClient()
    # Serialize each payload to JSON
    batch = [json.dumps(msg) for msg in messages]
    client.publish_batch(topic_name, batch)
    print(f"Published batch of {len(messages)} messages to {topic_name}")
