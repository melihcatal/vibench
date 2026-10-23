import os
from google.cloud import pubsub_v1

# Set environment variables for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'

def consume_event(project_id, subscription_id):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f'Received message: {message.data}')
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f'Listening for messages on {subscription_path}...')

    # Wrap subscriber in a 'with' block to automatically call close() to close the underlying gRPC channel when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result()
        except Exception as e:
            streaming_pull_future.cancel()
            print(f'Streaming pull future cancelled due to exception: {e}')

if __name__ == '__main__'):
    project_id = 'your-project-id'
    subscription_id = 'your-subscription-id'
    consume_event(project_id, subscription_id)