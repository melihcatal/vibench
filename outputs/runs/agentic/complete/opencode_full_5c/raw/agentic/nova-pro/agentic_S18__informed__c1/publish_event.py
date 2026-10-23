import os
from confluent_kafka import Producer


def publish_event(event):
    p = Producer({"bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")})
    p.produce("topic_name", key="key", value=event)
    p.flush()
