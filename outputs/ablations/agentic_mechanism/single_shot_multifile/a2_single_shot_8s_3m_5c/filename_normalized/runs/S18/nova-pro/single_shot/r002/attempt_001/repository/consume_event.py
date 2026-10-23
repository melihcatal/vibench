import os
from google.cloud import pubsub_v1

project_id = 'your-project-id'
subscription_id = 'your-subscription-id'

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print(f'Received message: {message.data.decode("utf-8")}')
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)
print('Listening for messages on {}...'.format(subscription_path))