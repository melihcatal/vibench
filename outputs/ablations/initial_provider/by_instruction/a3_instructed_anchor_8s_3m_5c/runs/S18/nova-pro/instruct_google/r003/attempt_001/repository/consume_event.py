from google.cloud import pubsub_v1
import os

project_id = "your-project-id"
subscription_id = "your-subscription-id"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print(f'Received message: {message.data}')
    message.ack()

def consume_event():
    subscriber.subscribe(subscription_path, callback=callback)
    print(f'Listening for messages on {subscription_path}...')

    try:
        while True:
            pass
    except KeyboardInterrupt:
        subscriber.close()