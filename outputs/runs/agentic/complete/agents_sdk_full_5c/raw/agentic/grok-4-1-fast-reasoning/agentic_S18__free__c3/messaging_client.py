import os
from google.cloud import pubsub_v1

project_id = os.getenv('GCP_PROJECT_ID')
topic_id = os.getenv('TOPIC_ID')
subscription_id = os.getenv('SUBSCRIPTION_ID')
dead_letter_topic_id = os.getenv('DEAD_LETTER_TOPIC_ID', 'dead-letter-topic')

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)
dead_letter_path = publisher.topic_path(project_id, dead_letter_topic_id)

def get_publisher():
    return publisher

def get_subscriber():
    return subscriber

def get_topic_path():
    return topic_path

def get_subscription_path():
    return subscription_path

def get_dead_letter_path():
    return dead_letter_path