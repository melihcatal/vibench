from google.cloud import pubsub_v1

def get_client(config):
    return pubsub_v1.PublisherClient(), pubsub_v1.SubscriberClient()

def get_topic_path(project_id, topic_id):
    return pubsub_v1.PublisherClient().topic_path(project_id, topic_id)

def get_subscription_path(project_id, subscription_id):
    return pubsub_v1.SubscriberClient().subscription_path(project_id, subscription_id)