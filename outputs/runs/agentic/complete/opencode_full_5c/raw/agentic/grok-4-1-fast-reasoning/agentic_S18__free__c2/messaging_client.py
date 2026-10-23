import os
from typing import Dict
from google.cloud import pubsub_v1
from google.api_core.retry import Retry
from messaging_models import PubSubMessage

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
if not project_id:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")

topic_id = os.getenv("PUBSUB_TOPIC_ID", "events-topic")
subscription_id = os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-sub")
dead_letter_topic_id = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-topic")

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()


def get_topic_path(topic: str = topic_id) -> str:
    return publisher.topic_path(project_id, topic)


def get_subscription_path(sub: str = subscription_id) -> str:
    return subscriber.subscription_path(project_id, sub)


def publish_message(topic: str, data: bytes, attributes: Dict[str, str] = None) -> str:
    if attributes is None:
        attributes = {}
    future = publisher.publish(get_topic_path(topic), data, **attributes)
    return future.result()


def pull_one_message(sub: str = subscription_id) -> Optional[PubSubMessage]:
    retry_policy = Retry(maximum=3)
    response = subscriber.pull(
        request={"subscription": get_subscription_path(sub), "max_messages": 1},
        retry=retry_policy,
    )
    if response.received_messages:
        received = response.received_messages[0]
        msg = PubSubMessage(
            data=received.message.data,
            message_id=received.message.message_id,
            attributes=dict(received.message.attributes),
            publish_time=received.message.publish_time.isoformat()
            if received.message.publish_time
            else "",
            ack_id=received.ack_id,
        )
        return msg
    return None


def ack_message(msg: PubSubMessage, sub: str = subscription_id):
    subscriber.acknowledge(
        request={"subscription": get_subscription_path(sub), "ack_ids": [msg.ack_id]}
    )
