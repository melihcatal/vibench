import os
from typing import Optional
from google.cloud import pubsub_v1
from messaging_models import EventMessage


def get_publisher_client() -> pubsub_v1.PublisherClient:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        return pubsub_v1.PublisherClient()
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        return pubsub_v1.SubscriberClient()
    return pubsub_v1.SubscriberClient()


def get_project_id() -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")


def get_topic_path(topic_name: str) -> str:
    project_id = get_project_id()
    publisher = pubsub_v1.PublisherClient()
    return publisher.topic_path(project_id, topic_name)


def get_subscription_path(subscription_name: str) -> str:
    project_id = get_project_id()
    subscriber = pubsub_v1.SubscriberClient()
    return subscriber.subscription_path(project_id, subscription_name)


def get_dead_letter_topic_path(dead_letter_topic_name: str) -> str:
    project_id = get_project_id()
    publisher = pubsub_v1.PublisherClient()
    return publisher.topic_path(project_id, dead_letter_topic_name)


def publish_message_to_topic(
    topic_name: str,
    event: EventMessage,
    attributes: Optional[dict] = None,
) -> str:
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_name)
    data = event.to_json().encode("utf-8")
    pub_attrs = {k: str(v) for k, v in (attributes or {}).items()}
    pub_attrs["event_type"] = event.event_type
    pub_attrs["event_id"] = event.event_id
    future = publisher.publish(topic_path, data, **pub_attrs)
    return future.result()


def consume_message_from_subscription(
    subscription_name: str,
    timeout: float = 10.0,
) -> Optional[tuple]:
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscription_name)
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        },
        timeout=timeout,
    )
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    ack_id = received.ack_id
    message = received.message
    return ack_id, message


def acknowledge_message(subscription_name: str, ack_id: str) -> None:
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscription_name)
    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [ack_id],
        }
    )


def nack_message(subscription_name: str, ack_id: str) -> None:
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscription_name)
    subscriber.modify_ack_deadline(
        request={
            "subscription": subscription_path,
            "ack_ids": [ack_id],
            "ack_deadline_seconds": 0,
        }
    )


def ensure_topic_exists(topic_name: str) -> str:
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_name)
    try:
        publisher.get_topic(request={"topic": topic_path})
    except Exception:
        publisher.create_topic(request={"name": topic_path})
    return topic_path


def ensure_subscription_exists(
    subscription_name: str,
    topic_name: str,
    dead_letter_topic_name: Optional[str] = None,
) -> str:
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscription_name)
    topic_path = get_topic_path(topic_name)
    try:
        subscriber.get_subscription(request={"subscription": subscription_path})
    except Exception:
        request = {
            "name": subscription_path,
            "topic": topic_path,
        }
        if dead_letter_topic_name:
            dl_topic_path = get_dead_letter_topic_path(dead_letter_topic_name)
            request["dead_letter_policy"] = {
                "dead_letter_topic": dl_topic_path,
                "max_delivery_attempts": 5,
            }
        subscriber.create_subscription(request=request)
    return subscription_path
