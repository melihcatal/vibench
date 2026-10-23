from google.cloud import pubsub_v1


def create_pubsub_client(project_id: str):
    """Creates a Pub/Sub client."""
    credentials = None
    # This is only needed if the environment is not already authenticated
    # credentials, project = google.auth.default()
    return pubsub_v1.PublisherClient(credentials=credentials), pubsub_v1.SubscriberClient(credentials=credentials)


def publish_message(project_id: str, topic_id: str, data: bytes):
    """Publishes a message to a Pub/Sub topic."""
    publisher, _ = create_pubsub_client(project_id)
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic_path, data)
    print(f'Published message ID: {future.result()}')


def subscribe_to_topic(project_id: str, subscription_id: str):
    """Subscribes to a Pub/Sub topic and prints received messages."""
    _, subscriber = create_pubsub_client(project_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f'Received message: {message.data}')
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f'Listening for messages on {subscription_path}...')

    # Wrap subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        try:
            streaming_pull_future.result()
        except Exception as e:
            streaming_pull_future.cancel()
            print(f'StreamingPull ended with exception: {e}')


def normalize_message(message: bytes) -> dict:
    """Normalizes a Pub/Sub message to a dictionary."""
    return {'data': message.decode('utf-8')}