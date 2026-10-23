import os
from google.cloud import pubsub_v1

def get_publisher():
    return pubsub_v1.PublisherClient()

def get_subscriber():
    return pubsub_v1.SubscriberClient()

def get_topic_path(project, topic):
    publisher = get_publisher()
    return publisher.topic_path(project, topic)

def get_subscription_path(project, subscription):
    subscriber = get_subscriber()
    return subscriber.subscription_path(project, subscription)