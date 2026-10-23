import os
from google.cloud import pubsub_v1

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

def get_publisher_client():
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    return pubsub_v1.SubscriberClient()

def topic_path(client, project_id, topic_id):
    return client.topic_path(project_id, topic_id)

def subscription_path(client, project_id, subscription_id):
    return client.subscription_path(project_id, subscription_id)