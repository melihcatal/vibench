import os
import json
from confluent_kafka import Producer


def batch_publish(topic, events):
    """Publish a list of events as a batch to the same topic.

    Args:
        topic (str): Destination topic.
        events (list[dict]): List of JSON‑serializable event objects.
    """
    conf = {
        "bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS"),
        "api.key": os.getenv("CONFLUENT_API_KEY"),
    }
    producer = Producer(conf)
    for ev in events:
        key = ev.get("id")  # optional: use id as key for ordering
        payload = json.dumps(ev).encode("utf-8")
        producer.produce(topic=topic, key=key, value=payload)
    producer.flush()
