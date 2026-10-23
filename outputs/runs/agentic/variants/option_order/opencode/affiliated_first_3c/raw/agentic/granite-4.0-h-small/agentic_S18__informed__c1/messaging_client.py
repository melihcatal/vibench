import os
from confluent_kafka import Producer, Consumer, KafkaError

# Broker configuration (IBM Event Streams or Confluent Cloud)
BOOTSTRAP_SERVERS = os.getenv("IBM_EVENT_STREAMS_BROKERS")
API_KEY = os.getenv("IBM_EVENT_STREAMS_APIKEY")


def create_producer():
    """Return a configured Kafka producer instance."""
    return Producer(
        {
            "bootstrap.servers": BOOTSTRAP_SERVERS,
            "api.key": API_KEY,
        }
    )


def create_consumer(group_id="my-consumer-group"):
    """Return a configured Kafka consumer instance."""
    return Consumer(
        {
            "bootstrap.servers": BOOTSTRAP_SERVERS,
            "api.key": API_KEY,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        }
    )


# Helper to safely produce a message


def produce(producer, topic, payload):
    try:
        message = payload.encode("utf-8")
        producer.produce(topic, message)
        producer.flush()
    except Exception as exc:
        print(f"Producer error: {exc}")


# Helper to consume messages


def consume_once(consumer, topic):
    consumer.subscribe([topic])
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        return None
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            return None
        else:
            print(f"Consumer error: {msg.error()}")
            return None
    return json.loads(msg.value().decode("utf-8"))


# Example helpers (optional)
if __name__ == "__main__":
    # Demo producer usage
    prod = create_producer()
    prod_example = {"id": "demo", "msg": "hello"}
    produce(prod, "my-events", json.dumps(prod_example))

    # Demo consumer usage
    cons = create_consumer()
    msg = consume_once(cons, "my-events")
    print("Consumed:", msg)

    # Cleanup
    prod.close()
    cons.close()
