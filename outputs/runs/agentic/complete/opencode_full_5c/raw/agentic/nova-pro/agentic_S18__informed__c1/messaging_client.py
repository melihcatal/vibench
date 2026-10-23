import os
from confluent_kafka import Producer, Consumer


def get_producer():
    return Producer({"bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")})


def get_consumer():
    return Consumer(
        {
            "bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS"),
            "group.id": "mygroup",
            "auto.offset.reset": "earliest",
        }
    )
