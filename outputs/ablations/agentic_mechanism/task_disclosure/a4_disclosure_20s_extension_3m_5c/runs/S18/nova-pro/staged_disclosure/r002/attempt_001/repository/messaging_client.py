from google.cloud import pubsub_v1

# Local configuration
project_id = 'your-project-id'

# Helper utilities
def create_topic(topic_name):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    publisher.create_topic(request={'name': topic_path})
    print(f'Topic {topic_name} created.')

def publish_message(topic_name, message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    future = publisher.publish(topic_path, message.encode('utf-8'))
    print(f'Message published: {future.result()}')

def create_subscription(subscription_name, topic_name):
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    subscriber.create_subscription(request={'name': subscription_path, 'topic': topic_path})
    print(f'Subscription {subscription_name} created.')

def pull_messages(subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    response = subscriber.pull(request={'subscription': subscription_path, 'max_messages': 10})
    for received_message in response.received_messages:
        print(f'Message: {received_message.message.data.decode(