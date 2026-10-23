import os
from google.cloud import pubsub_v1
from google.api_core import retry

project_id = os.environ["GCP_PROJECT_ID"]
topic_id = os.getenv("GCP_TOPIC_ID", "events-topic")
sub_id = os.getenv("GCP_SUB_ID", "events-sub")
dl_topic_id = os.getenv("GCP_DL_TOPIC_ID", "dead-letter-topic")

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

topic_path = publisher.topic_path(project_id, topic_id)
sub_path = subscriber.subscription_path(project_id, sub_id)
dl_path = publisher.topic_path(project_id, dl_topic_id)


def publish(topic_path, data: bytes, attributes: dict = None):
    if attributes is None:
        attributes = {}
    api_future = publisher.publish(topic_path, data, **attributes)
    message_id = api_future.result()
    return message_id


def consume_one():
    response = subscriber.pull(subscription=sub_path, max_messages=1, timeout=10.0)
    if not response.received_messages:
        return None
    return response.received_messages[0]


def ack(ack_id):
    subscriber.acknowledge(subscription=sub_path, ack_ids=[ack_id])
