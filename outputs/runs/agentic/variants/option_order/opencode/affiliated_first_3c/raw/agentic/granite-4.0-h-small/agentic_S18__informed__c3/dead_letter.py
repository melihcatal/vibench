import os
from confluent_kafka import Producer

dead_letter_topic = os.getenv("DEAD_LETTER_TOPIC", "dead-letter")
bootstrap_servers = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
api_key = os.getenv("CONFLUENT_API_KEY")

cfg = {
    "bootstrap.servers": bootstrap_servers,
    "api.key": api_key,
}
dl_producer = Producer(cfg)


def send_to_dead_letter(original_topic, original_key, original_value):
    """Send a failed message to a dead-letter topic with metadata.

    Args:
        original_topic (str): Topic where delivery failed.
        original_key (str|None): Original message key.
        original_value (bytes|dict): Original message payload.
    """
    metadata = {
        "original_topic": original_topic,
        "original_key": original_key,
        "delivery_attempt": 1,  # can be incremented on retries
    }
    payload = {
        "metadata": metadata,
        "payload": original_value,
    }
    dl_producer.produce(
        topic=dead_letter_topic,
        key=original_key,
        value=json.dumps(payload).encode("utf-8"),
    )
    dl_producer.flush()
