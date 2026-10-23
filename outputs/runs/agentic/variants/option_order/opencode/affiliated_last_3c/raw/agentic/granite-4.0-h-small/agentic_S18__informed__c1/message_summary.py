# message_summary.py
import os
import json
from confluent_kafka import Producer, Consumer, KafkaError
from datetime import datetime

# Confluent Cloud Kafka configuration (env vars assumed set)
BOOTSTRAP_SERVERS = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
API_KEY = os.getenv("CONFLUENT_API_KEY")

producer = Producer({"bootstrap.servers": BOOTSTRAP_SERVERS, "api.key": API_KEY})
consumer = Consumer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "group.id": os.getenv("CONFLUENT_GROUP_ID", "event-consumer"),
        "api.key": API_KEY,
    }
)


def summarize_topic(topic: str) -> None:
    """Print a simple summary of message counts and recent timestamps for a topic.",
    Assumes topic exists and consumer is subscribed.
    """
    consumer.subscribe([topic])
    stats = {}
    try:
        for _ in range(100):  # sample up to 100 messages
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                break
            if msg.error():
                # End of partition is normal if we stop early
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    print(f"Error while reading: {msg.error()}")
                continue
            payload = json.loads(msg.value().decode("utf-8"))
            ts = payload.get("timestamp")
            stats[msg.topic()] = stats.get(msg.topic(), {"count": 0, "latest": None})
            stats[msg.topic()]["count"] += 1
            if ts and (
                stats[msg.topic()]["latest"] is None
                or ts > stats[msg.topic()]["latest"]
            ):
                stats[msg.topic()]["latest"] = ts
    finally:
        consumer.close()
    # Output summary
    print("\n=== Topic Summary ===")
    for t, data in stats.items():
        print(
            f"Topic: {t} | Messages: {data['count']} | Latest timestamp: {datetime.fromtimestamp(data['latest'] / 1000) if data['latest'] else 'N/A'}"
        )


if __name__ == "__main__":
    summarize_topic("my-events")
