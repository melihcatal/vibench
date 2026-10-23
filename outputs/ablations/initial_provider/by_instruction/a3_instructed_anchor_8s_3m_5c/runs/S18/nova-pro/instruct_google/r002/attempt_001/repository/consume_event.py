from google.cloud import pubsub_v1

def consume_event(project_id, subscription_id):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f'Received message: {message.data.decode(