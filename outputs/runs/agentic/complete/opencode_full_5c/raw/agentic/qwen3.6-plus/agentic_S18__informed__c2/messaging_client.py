import os
from google.cloud import pubsub_v1
from messaging_models import MessagingConfig, EventMessage


def load_config() -> MessagingConfig:
    return MessagingConfig.from_env()


def get_publisher_client() -> pubsub_v1.PublisherClient:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    if credentials_path:
        return pubsub_v1.PublisherClient()
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    if credentials_path:
        return pubsub_v1.SubscriberClient()
    return pubsub_v1.SubscriberClient()


def build_topic_path(config: MessagingConfig) -> str:
    return f"projects/{config.project_id}/topics/{config.topic_id}"


def build_subscription_path(config: MessagingConfig) -> str:
    return f"projects/{config.project_id}/subscriptions/{config.subscription_id}"


def build_dead_letter_topic_path(config: MessagingConfig) -> str:
    return f"projects/{config.project_id}/topics/{config.dead_letter_topic_id}"


def publish_raw_message(
    publisher: pubsub_v1.PublisherClient,
    topic_path: str,
    payload_bytes: bytes,
    attributes: dict | None = None,
) -> str:
    future = publisher.publish(topic_path, data=payload_bytes, **(attributes or {}))
    return future.result()


def pull_one_message(
    subscriber: pubsub_v1.SubscriberClient,
    subscription_path: str,
    max_messages: int = 1,
) -> list:
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": max_messages,
        }
    )
    return list(response.received_messages)


def acknowledge_message(
    subscriber: pubsub_v1.SubscriberClient,
    subscription_path: str,
    ack_id: str,
) -> None:
    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [ack_id],
        }
    )


def modify_ack_deadline(
    subscriber: pubsub_v1.SubscriberClient,
    subscription_path: str,
    ack_id: str,
    deadline_seconds: int = 0,
) -> None:
    subscriber.modify_ack_deadline(
        request={
            "subscription": subscription_path,
            "ack_ids": [ack_id],
            "ack_deadline_seconds": deadline_seconds,
        }
    )


def parse_received_message(received_msg) -> EventMessage:
    data = received_msg.message.data.decode("utf-8")
    attributes = dict(received_msg.message.attributes)
    event = EventMessage.from_json(data)
    event.attributes.update(attributes)
    return event
