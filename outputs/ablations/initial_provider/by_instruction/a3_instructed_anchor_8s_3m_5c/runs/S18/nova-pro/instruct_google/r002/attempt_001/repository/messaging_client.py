from google.cloud import pubsub_v1

def get_publisher_client(project_id):
    return pubsub_v1.PublisherClient()

def get_subscriber_client(project_id):
    return pubsub_v1.SubscriberClient()