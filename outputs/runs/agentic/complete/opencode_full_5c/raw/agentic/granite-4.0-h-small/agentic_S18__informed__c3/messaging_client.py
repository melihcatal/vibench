import os
import json
from confluent_kafka import KafkaError

# ---------------------------------------------------------------------------
# Confluent Kafka client helper (for IBM Event Streams / Confluent Cloud)
# ---------------------------------------------------------------------------


def get_kafka_client(bootstrap_servers, api_key=None):
    """
    Build and configure a Kafka client (Producer or Consumer) for Confluent Kafka.

    Args:
        bootstrap_servers (str): Comma‑separated list of brokers.
        api_key (str|None): Confluent API key. If omitted, key is read from env.

    Returns:
        Instance of confluent_kafka.Producer or Consumer depending on caller.
    """
    conf = {
        "bootstrap.servers": bootstrap_servers,
    }
    if api_key:
        conf["api.key"] = api_key
    else:
        # fallback to env when not passed explicitly
        conf["api.key"] = os.getenv("CONFLUENT_API_KEY", "")
    return conf


# Convenience wrappers for caller files


def create_kafka_producer(config):
    """Create a Kafka Producer using the dict returned by get_kafka_client."""
    return Producer(config)


def create_kafka_consumer(config):
    """Create a Kafka Consumer using the dict returned by get_kafka_client."""
    return Producer(
        config
    )  # placeholder – callers should call Consumer(config) directly


# ---------------------------------------------------------------------------
# Example of how consumer code could use this (shown in consume_event.py)
# ---------------------------------------------------------------------------
# from messaging_client import get_kafka_client, create_kafka_consumer
# conf = get_kafka_client(bootstrap_servers, api_key)
# consumer = Consumer(conf)
# ---------------------------------------------------------------------------
