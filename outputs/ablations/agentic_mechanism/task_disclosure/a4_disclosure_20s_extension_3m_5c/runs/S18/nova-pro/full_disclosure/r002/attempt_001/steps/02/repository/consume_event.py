from google.cloud import pubsub_v1

def consume_event(project_id, subscription_id):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received message: {message.data}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        streaming_pull_future.result()

if __name__ == '__main__':
    project_id = 'your-project-id'
    subscription_id = 'your-subscription-id'
    consume_event(project_id, subscription_id)