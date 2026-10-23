from google.cloud import pubsub_v1


def create_pubsub_client():
    return pubsub_v1.PublisherClient()


def publish_message(project_id, topic_id, data):
    client = create_pubsub_client()
    topic_path = client.topic_path(project_id, topic_id)
    data = data.encode('utf-8')
    future = client.publish(topic_path, data)
    print(f'Published message ID: {future.result()}')


def subscribe_to_topic(project_id, subscription_id):
    client = create_pubsub_client()
    subscription_path = client.subscription_path(project_id, subscription_id)
    print(f'Listening for messages on {subscription_path}')

    def callback(message):
        print(f'Received message: {message.data}')
        message.ack()

    client.subscribe(subscription_path, callback=callback)


def normalize_message(message):
    return message.decode('utf-8')