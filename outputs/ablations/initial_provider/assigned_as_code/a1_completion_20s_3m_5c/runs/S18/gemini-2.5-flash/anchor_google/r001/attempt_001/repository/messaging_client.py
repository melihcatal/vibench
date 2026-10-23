from google.cloud import pubsub_v1
import os

def get_publisher_client():
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    return pubsub_v1.SubscriberClient()

def get_project_id():
    return os.getenv("GOOGLE_CLOUD_PROJECT_ID")

def get_topic_path(client, topic_id):
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return client.topic_path(project_id, topic_id)

def get_subscription_path(client, subscription_id):
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return client.subscription_path(project_id, subscription_id)
