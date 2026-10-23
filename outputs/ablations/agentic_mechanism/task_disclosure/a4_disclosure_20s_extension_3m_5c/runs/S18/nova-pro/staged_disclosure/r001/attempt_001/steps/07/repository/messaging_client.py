from google.cloud import pubsub_v1

# Local configuration
project_id = 'your-project-id'

# Client helper utilities
def create_topic(topic_name):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    topic = publisher.create_topic(request={'name': topic_path})
    print(f'Topic {topic.name} created.')

def publish_message(topic_name, message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    future = publisher.publish(topic_path, message.encode('utf-8'))
    print(f'Published message ID: {future.result()}')

def create_subscription(subscription_name, topic_name):
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    subscription = subscriber.create_subscription(request={'name': subscription_path, 'topic': topic_path})
    print(f'Subscription {subscription.name} created.')

def receive_messages(subscription_name):
    def callback(message):
        print(f'Received message: {message.data.decode(