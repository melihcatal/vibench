import os, json, base64
from confluent_kafka import Producer

bootstrap_servers = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
api_key = os.getenv("CONFLUENT_API_KEY")

conf = {
    "bootstrap.servers": bootstrap_servers,
    "api.key": api_key,
}
producer = Producer(conf)


def publish_event(topic, event):
    """Publish a single JSON event to the given topic.

    Args:
        topic (str): Topic name.
        event (dict): JSON‑serializable event payload.
    """
    payload = json.dumps(event).encode("utf-8")
    producer.produce(topic=topic, value=payload, on_delivery=handle_delivery)
    producer.flush()


def handle_delivery(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered message to {msg.topic()}[{msg.partition()}]: {msg.key()}")
