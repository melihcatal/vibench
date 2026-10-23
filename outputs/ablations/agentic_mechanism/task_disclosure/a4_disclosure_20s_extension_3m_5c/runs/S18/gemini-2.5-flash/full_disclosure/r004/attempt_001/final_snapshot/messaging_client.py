from google.cloud import pubsub_v1
import os

def get_publisher_client():
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    return pubsub_v1.SubscriberClient()

def get_project_id():
    return os.environ.get("GOOGLE_CLOUD_PROJECT")

def get_topic_path(project_id, topic_id):
    return pubsub_v1.PublisherClient.topic_path(project_id, topic_id)

def get_subscription_path(project_id, subscription_id):
    return pubsub_v1.SubscriberClient.subscription_path(project_id, subscription_id)
