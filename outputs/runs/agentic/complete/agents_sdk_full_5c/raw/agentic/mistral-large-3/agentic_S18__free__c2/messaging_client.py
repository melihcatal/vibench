import os
from google.cloud import pubsub_v1

def get_pubsub_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()

def get_pubsub_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()

def acknowledge_message(subscriber: pubsub_v1.SubscriberClient, subscription_path: str, ack_id: str) -> None:
    subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [ack_id]})

def nack_message(subscriber: pubsub_v1.SubscriberClient, subscription_path: str, ack_id: str) -> None:
    subscriber.modify_ack_deadline(request={"subscription": subscription_path, "ack_ids": [ack_id], "ack_deadline_seconds": 0})