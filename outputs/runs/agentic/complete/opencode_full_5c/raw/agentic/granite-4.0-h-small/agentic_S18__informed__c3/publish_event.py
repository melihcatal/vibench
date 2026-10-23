import os
from confluent_kafka import Producer
from messaging_client import get_kafka_client

# Confluent Kafka (IBM Event Streams / Confluent Cloud)
bootstrap_servers = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
api_key = os.getenv("CONFLUENT_API_KEY")

producer = get_kafka_client(bootstrap_servers)

producer.configure({"api.key": api_key})


def publish_event(topic, event):
    """Publish a JSON event to the specified topic.
    Args:
        topic (str): Topic name.
        event (dict): JSON-serializable event payload.
    """
    try:
        producer.produce(topic=topic, value=str(event))
        producer.flush()
        print(f"Published event to {topic}")
    except Exception as e:
        print(f"Failed to publish event: {e}")


if __name__ == "__main__":
    # Example usage (remove in production)
    sample_event = {"id": "evt_001", "payload": {"message": "Hello Pub/Sub"}}
    publish_event("my_topic", sample_event)
