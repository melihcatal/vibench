from google.cloud import pubsub_v1

# Configuration
project_id = 'your-project-id'

# Client setup
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

# Helper functions
def create_topic(topic_name):
    topic_path = publisher.topic_path(project_id, topic_name)
    publisher.create_topic(request={'name': topic_path})
    print(f'Topic {topic_name} created.')

def publish_message(topic_name, data):
    topic_path = publisher.topic_path(project_id, topic_name)
    data = data.encode('utf-8')
    publisher.publish(topic=topic_path, data=data)
    print(f'Message published to {topic_name}.')

def subscribe_to_topic(subscription_name, callback):
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    subscriber.subscribe(subscription_path, callback=callback)
    print(f'Subscribed to {subscription_name}.')

def callback(message):
    print(f'Received message: {message.data.decode(