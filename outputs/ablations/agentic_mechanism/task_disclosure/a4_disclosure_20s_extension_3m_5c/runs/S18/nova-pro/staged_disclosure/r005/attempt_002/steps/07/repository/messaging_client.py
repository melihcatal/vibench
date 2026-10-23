from google.cloud import pubsub_v1

# Local configuration
project_id = 'your-project-id'
topic_id = 'your-topic-id'
subscription_id = 'your-subscription-id'

# Create a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

# Helper function to create a topic
def create_topic():
    topic_path = publisher.topic_path(project_id, topic_id)
    publisher.create_topic(request={'name': topic_path})
    print(f'Topic {topic_id} created.')

# Helper function to create a subscription
def create_subscription():
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    subscriber.create_subscription(request={'name': subscription_path, 'topic': topic_path})
    print(f'Subscription {subscription_id} created.')

# Helper function to publish a message
def publish_message(data):
    topic_path = publisher.topic_path(project_id, topic_id)
    data = data.encode('utf-8')
    future = publisher.publish(topic_path, data)
    print(f'Published message ID: {future.result()}')

# Helper function to receive messages
def receive_messages():
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    def callback(message):
        print(f'Received message: {message.data.decode(