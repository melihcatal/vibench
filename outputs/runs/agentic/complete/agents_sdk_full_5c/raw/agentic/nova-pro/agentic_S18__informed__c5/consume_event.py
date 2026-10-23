import os
from google.cloud import pubsub_v1

# Configuration
project_id = 'your-project-id'
subscription_id = 'your-subscription-id'

# Authenticate
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print(f'Received message: {message.data}')
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)