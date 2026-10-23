from messaging_client import PubSubClient


def dead_letter(original_topic, dlq_topic, message):
    """Send a failed message to a dead‑letter topic.

    Args:
        original_topic (str): The topic where publishing originally failed.
        dlq_topic (str): The configured dead‑letter topic.
        message (dict): Original message data.
    """
    client = PubSubClient()  # Google Cloud Pub/Sub provider
    json_msg = json.dumps(message)
    client.publish(dlq_topic, json_msg)
    print(f"Dead‑lettered message from {original_topic} to {dlq_topic}")
