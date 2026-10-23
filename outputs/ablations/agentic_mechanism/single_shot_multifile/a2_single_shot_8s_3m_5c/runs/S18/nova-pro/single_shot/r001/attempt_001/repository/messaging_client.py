import os
from google.cloud import pubsub_v1

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

def get_publisher_client():
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    return pubsub_v1.SubscriberClient()

def get_topic_path(publisher, topic_id):
    return publisher.topic_path(project_id, topic_id)

def get_subscription_path(subscriber, subscription_id):
    return subscriber.subscription_path(project_id, subscription_id)