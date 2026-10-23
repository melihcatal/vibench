import os
from google.cloud import pubsub_v1

# Set up environment variables for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'

# Create a publisher client
publisher = pubsub_v1.PublisherClient()

# Create a subscriber client
subscriber = pubsub_v1.SubscriberClient()

# Helper function to publish a message
def publish_message(topic_name, message):
    topic_path = publisher.topic_path('your-project-id', topic_name)
    data = message.encode('utf-8')
    publisher.publish(topic_path, data)

# Helper function to subscribe to a topic
def subscribe_to_topic(subscription_name, callback):
    subscription_path = subscriber.subscription_path('your-project-id', subscription_name)
    subscriber.subscribe(subscription_path, callback=callback)