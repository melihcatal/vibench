from google.cloud import pubsub_v1

def create_publish_request(topic_name, messages):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('your-project-id', topic_name)
    future = publisher.publish(topic_path, messages)
    return future

def create_subscribe_request(subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path('your-project-id', subscription_name)
    return subscriber.pull(subscription_path)

def normalize_message(message):
    return message.data.decode('utf-8')