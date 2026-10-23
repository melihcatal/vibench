from google.cloud import pubsub_v1


def get_pubsub_client(project_id):
    return pubsub_v1.SubscriberClient()