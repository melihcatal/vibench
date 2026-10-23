import os
from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(os.getenv('GCP_PROJECT'), os.getenv('GCP_SUBSCRIPTION'))

def callback(message):
    print(f'Received {message.data}.')
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}...')