import os
from confluent_kafka import Consumer


def consume_event():
    c = Consumer(
        {
            "bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS"),
            "group.id": "mygroup",
            "auto.offset.reset": "earliest",
        }
    )
    c.subscribe(["topic_name"])
    msg = c.poll(1.0)
    if msg is None:
        return None
    if msg.error():
        return None
    return msg.value().decode("utf-8")
