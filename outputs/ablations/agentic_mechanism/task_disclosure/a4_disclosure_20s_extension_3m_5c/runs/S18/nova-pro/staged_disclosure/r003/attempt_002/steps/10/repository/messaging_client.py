from google.cloud import pubsub_v1

project_id = 'your-project-id'
topic_id = 'your-topic-id'
subscription_id = 'your-subscription-id'

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def publish_message(data):
    data = data.encode('utf-8')
    future = publisher.publish(topic_path, data)
    print(f'Published message ID: {future.result()}')

def receive_messages(callback):
    def message_callback(message):
        print(f'Received message: {message.data}')
        callback(message)
        message.ack()
    streaming_pull_future = subscriber.subscribe(subscription_path, message_callback)
    print(f'Listening for messages on {subscription_path}...')
    with subscriber:
        streaming_pull_future.result()

if __name__ == '__main__':
    publish_message('Hello, Pub/Sub!')
    receive_messages(lambda message: None)