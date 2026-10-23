import os
from google.cloud import pubsub_v1

# Set environment variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/service-account-file.json'

# Initialize Pub/Sub client
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('my-project-id', 'my-subscription')

# Define callback function
def callback(message):
    print(f'Received message: {message.data}')
    message.ack()

# Start listening for messages
subscriber.subscribe(subscription_path, callback=callback)