import os
from confluent_kafka import Producer


def batch_publish(messages):
    p = Producer({"bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")})
    for message in messages:
        p.produce("topic_name", key="key", value=message)
    p.flush()
