import os
from google.cloud import pubsub_v1

# Set up the Pub/Sub client
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

# Define the topic and subscription
project_id = "your-project-id"
topic_id = "your-topic-id"
subscription_id = "your-subscription-id"

topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)
