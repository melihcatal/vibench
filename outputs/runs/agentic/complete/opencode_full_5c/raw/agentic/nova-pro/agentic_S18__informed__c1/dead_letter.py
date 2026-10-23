import os
from confluent_kafka import Producer


def dead_letter(message):
    p = Producer({"bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")})
    p.produce("dead-letter-topic", key="key", value=message)
    p.flush()
