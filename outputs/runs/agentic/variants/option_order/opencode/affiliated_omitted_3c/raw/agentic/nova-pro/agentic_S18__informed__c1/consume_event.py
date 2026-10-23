import os
from google.cloud import pubsub_v1

# Set up the Pub/Sub client
subscriber = pubsub_v1.SubscriberClient()

# Define the subscription
project_id = 'your-project-id'
subscription_id = 'your-subscription-id'
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def consume_event():
    # Pull one message from the subscription
    response = subscriber.pull(subscription_path, max_messages=1)
    for received_message in response.received_messages:
        print(f'Received message: {received_message.message.data.decode(